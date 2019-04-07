# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JDItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #名字
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #店铺
    store = scrapy.Field()
    #评论条数
    evaluate_num = scrapy.Field()
    #商品url
    detail_url = scrapy.Field()
    #提供商
    support = scrapy.Field()
    #一级分类
    first_class = scrapy.Field()
    #二级分类
    second_class = scrapy.Field()
    #图片链接
    img_url = scrapy.Field()
