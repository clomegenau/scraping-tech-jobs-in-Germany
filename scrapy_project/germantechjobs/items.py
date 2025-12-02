# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# this class is a test remove it when you commit to writing this spider
class ArbeitsAgenTur(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    full_time = scrapy.Field()
    ref_number = scrapy.Field()
    apply_for_this_job = scrapy.Field()
    url = scrapy.Field()




