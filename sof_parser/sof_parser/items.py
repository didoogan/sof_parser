# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    q_author = scrapy.Field()
    q_text = scrapy.Field()
    q_votes = scrapy.Field()
    q_data = scrapy.Field()
    a_author = scrapy.Field()
    a_data = scrapy.Field()
    a_votes = scrapy.Field()
    a_link = scrapy.Field()

