# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsStartup(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
    apply_for_this_job = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    pass

# this class is a test remove it when you commit to writing this spider
class ArbeitsAgenTur(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    tags = scrapy.Field()
    full_time = scrapy.Field()
    ref_number = scrapy.Field()
    apply_for_this_job = scrapy.Field()
    url = scrapy.Field()




