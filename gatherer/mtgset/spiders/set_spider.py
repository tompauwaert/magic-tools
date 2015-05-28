# -*- coding: utf-8 -*-
"""
Spider that downloads images of a few particular sets.
The sets to be downloaded, their codes will be provided as command line parameters to the spider.
The urls they can be downloaded from have to be read by using the set_downloaders.SetManager.
"""
import re
import scrapy
import gatherer.set_manager
import gatherer.mtgset.items


class SetSpider(scrapy.Spider):

    name = "set-spider"
    allowed_domains = ["http://magiccards.info"]
    language_codes = "[en]"

    def __init__(self, code_list=[], *args, **kwargs):
        """
        Initialize the set spider. The set spider crawls one set at a time and downloads
        all relevant information of that set.\n
        :param code_list: comma-separated list of all the sets to download. Set codes accepted
        as parameters are the official set codes (mtgjson.com)
        :param args:
        :param kwargs:
        :return:
        """
        super(SetSpider, self).__init__(*args, **kwargs)

        if code_list is None:
            raise ValueError("Must provide a minimum of one set code to crawl.")
        else:
            codes = code_list

        manager = gatherer.set_manager.SetManager()
        manager.read_sets_mcinfo()
        manager.read_sets_original()

        self.mci_codes = [manager.map_code(code, manager.CODE, manager.MCICODE) for code in codes]
        self.start_urls = [manager.get_mci_set_info(mciCode)["url"] for mciCode in self.mci_codes]


    def parse(self, response):
        """
        Parse the set URLS. The URLS to be parsed by this spider are either 'set' urls or 'card' urls..
        Set URLS are set pages that, after parsing, will generate a request URL for each image on the page.

        TODO: Save downloading progress.

        :param response:
        :return:
        """
        set_url = r".*magiccards.info/\w+/" + re.escape(self.language_codes) + r"\.html"
        card_url = r".*magiccards.info/\w+/" + re.escape(self.language_codes) + r"/\d+.html"

        item = gatherer.mtgset.items.SimplePrint()
        item.field = {}
        item['set'] = set_url
        item['card'] = card_url
        return item


















