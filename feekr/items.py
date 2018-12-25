# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DetailItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field() #所有图片
    images = scrapy.Field()

    title = scrapy.Field()
    userName = scrapy.Field()
    userImg = scrapy.Field()
    address = scrapy.Field()
    passageList = scrapy.Field()
    imageMap = scrapy.Field() #key内容图片, value 内容图片描述
    pass


class FeekrItem(scrapy.Item):
    pass