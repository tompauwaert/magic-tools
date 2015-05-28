"""
This file defines a crawler worker that may be used to launch scrapy
spiders from a python script.
Source code from: http://blog.tryolabs.com/2011/09/27/calling-scrapy-python-script/
"""
import copy
import pprint
import scrapy.cmdline
from scrapy import signals
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing import Process

class CrawlerWorker(Process):

    def __init__(self, spider, result_list, settings=None):
        Process.__init__(self)
        self.result_queue = result_list

        if settings is None:
            settings = Settings()

        self.crawler = CrawlerProcess(settings)
        self.crawler.create_crawler(spider.__class__.__name__)
        self.crawler.crawlers['spider'] = spider
        self.spider = spider
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)
        print "here"

    def run(self):
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)

default_settings = {
    "BOT_NAME" : "gatherer",
    "USER_AGENT" : "gatherer",
    "CONCURRENT_REQUESTS_PER_DOMAIN" : "1",
    "DOWNLOAD_DELAY" : "0",
}

def run_crawler(spider='', arguments=[], settings={}):
    """
    Run a crawler in a its own separate process.\n
    :param spider: The spider to be run while for crawling. This must be a valid spider.
    :param result_list: A list used for storing all the results (items) of the spider.
    If no queue is specified, then run_crawler can be iterated over and return the results
    one at a time. \n
    :param settings: Settings to use for the crawling.\n
    :return: Nothing if a result queue is given. The function becomes iterable if no result_list is given.\n
    """
    # if spider is None:
    #     raise ValueError("run_crawler expects a valid spider.")
    # if result_list is None:
    #     no_list = True
    #     result_list = []
    # else:
    #     no_list = False
    #
    # print "run_crawler.start()"
    # crawler = CrawlerWorker(spider, result_list, settings)
    # crawler.start()
    # crawler.join()
    # print "run_crawler.done"
    #
    # if no_list:
    #     return result_list

    arguments_list = []
    for arg in arguments:
        arguments_list.append('-a')
        arguments_list.append(arg)

    local_settings = copy.deepcopy(default_settings)
    for setting, value in settings.iteritems():
        local_settings[setting] = value

    settings_list = []
    for key, value in local_settings.iteritems():
        settings_list.append('-s')
        settings_list.append("{}={}".format(key, value))

    args_for_scrapy = [
        'scrapy',
        'runspider',
    ]
    args_for_scrapy.append(spider)
    args_for_scrapy.extend(arguments_list)
    args_for_scrapy.extend(settings_list)
    scrapy.cmdline.execute(args_for_scrapy)
    # pprint.pprint(args_for_scrapy)







