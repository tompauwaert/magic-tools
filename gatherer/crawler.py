"""
This file defines a crawler worker that may be used to launch scrapy
spiders from a python script.
Source code from: http://blog.tryolabs.com/2011/09/27/calling-scrapy-python-script/
"""

from scrapy import signals
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
import multiprocessing

class CrawlerWorker(multiprocessing.Process):

    def __init__(self, spider, result_queue, settings=None):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue

        if settings is None:
            settings = Settings()

        self.crawler = CrawlerProcess(settings)
        self.crawler.crawlers['spider'] = spider
        self.spider = spider
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)



