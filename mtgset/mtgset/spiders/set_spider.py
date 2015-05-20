# -*- coding: utf-8 -*-
"""
Spider that downloads images of a few particular sets.
The sets to be downloaded, their codes will be provided as command line parameters to the spider.
The urls they can be downloaded from have to be read by using the set_downloaders.SetManager.
"""
from __future__ import absolute_import
from mtgset.set_downloader import SetManager
import scrapy


class SetSpider(scrapy.Spider):

    name = "set-spider"
    allowed_domains = ["http://magiccards.info"]

    def __init__(self, code_list="", *args, **kwargs):
        super(SetSpider, self).__init__(*args, **kwargs)

        codes = code_list.split(',')
        self.start_urls = []

        manager = SetManager()
        manager.read_sets_mcinfo()
        manager.read_sets_original()

        mciCodes = []



    def start_requests(self):
        """
       Makes a request url for each set code given to the spider for downloading.
        :return:
        """
        pass

    def parse(self, response):
        pass
