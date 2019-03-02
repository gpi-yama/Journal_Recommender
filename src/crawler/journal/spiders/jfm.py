# -*- coding: utf-8 -*-
import scrapy
from journal.items import JournalItem


class JfmSpider(scrapy.Spider):
    name = 'jfm'
    allowed_domains = ['cambridge.org']
    start_urls = [
        'https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/listing']
    _num = 2

    def parse(self, response):
        for select in response.css("div.representation.overview.search"):
            item = JournalItem()
            item["title"] = select.css("li.title a.part-link::text").extract()
            item["author"] = select.css(
                "li.author a.more-by-this-author::text").extract()
            item["date"] = select.css("li.published span.date::text").extract()
            item["abstract"] = select.css(
                "li.no-margin-top.abstract p::text").extract()
            item["url"] = select.css(
                "li.source a.url.doi::text"
            ).extract()
            item["jname"] = select.css(
                "li.source a.productParent::text").extract()

            yield item

        name = 'a[href="?pageNum=' + str(self._num) + '"]'
        next_page = response.css(name).xpath("@href").extract_first()
        print("next page is", next_page)
        if next_page is not None:
            self._num += 1
            print("OKOK")
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
