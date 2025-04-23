# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IaScraperItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    summary = scrapy.Field()
    published_at = scrapy.Field()
    source = scrapy.Field()
    domain = scrapy.Field()