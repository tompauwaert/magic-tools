# -*- coding: utf-8 -*-

from __future__ import absolute_import
from scrapy.spider import BaseSpider
from ..items import Set

""" TODO:
1. Read other sets as well:
    a. Special sets
    b. MTGO
    c. Promo Cards
2. Read other languages as well:
    a. German, French, Italian, Spanish, Portuguese, Japanese, Chinese, Russian,
        Taiwanese, Korean
"""

class MagicSpider(BaseSpider):
    name = "magic"
    allowed_domains = ["http://magiccards.info"]
    start_urls = [
        "http://magiccards.info/sitemap.html"
    ]

    def parse(self, response):
        block_html_list = response.xpath("/html/body/table[2]/tr/td[1]/ul/li")
        for block_html in block_html_list:
            for set_html in block_html.xpath("ul/li"):
                item = Set()
                item['name'] = set_html.xpath("a/text()").extract()
                item['url'] = set_html.xpath("a/@href").extract()
                item['code'] = set_html.xpath("small/text()").extract()
                yield item
