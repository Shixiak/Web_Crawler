# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionItem(scrapy.Item):
    text_analysis = scrapy.Field()
    content = scrapy.Field()
    p_list = scrapy.Field()
    p_name = scrapy.Field()
