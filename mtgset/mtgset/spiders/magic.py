# -*- coding: utf-8 -*-

from __future__ import absolute_import
from scrapy.spider import BaseSpider
from ..items import Block


class MagicSpider(BaseSpider):
    name = "magic"
    allowed_domains = ["http://magiccards.info"]
    start_urls = [
        "http://magiccards.info/sitemap.html"
    ]

    def parse(self, response):
        block_html_list = response.xpath("/html/body/table[2]/tr/td[1]/ul/li")
        for block_html in block_html_list:
            item = Block()
            item['name'] = block_html.xpath("./text()[first()]").extract()
            item['sets'] = {}
            counter = 0
            for set_html in block_html.xpath("/ul/li"):
                item[counter] = {}
                item[counter]['name'] = set_html.xpath("/a/text()").extract()
                item[counter]['url'] = set_html.xpath("/a/@href").extract()
                item[counter]['code'] = set_html.xpath("/small/text()").extract()
            yield item
