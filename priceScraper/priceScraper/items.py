# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class cotoItem(scrapy.Item):
    product_id = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()