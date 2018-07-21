# -*- coding: utf-8 -*-
# ------------------------------------------
#   版本：1.0
#   日期：2018-07-19
#   作者：xishu
# ------------------------------------------
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DpSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shop_url = scrapy.Field() #店铺ID
    shop_name = scrapy.Field()#店铺名称
    menu = scrapy.Field()#推荐菜
    shop_kind = scrapy.Field()#菜系
    mall = scrapy.Field() #商圈
    avg_fee = scrapy.Field() #人均
    address = scrapy.Field()#地址
    shop_brand = scrapy.Field()# 是否分店
    service_type = scrapy.Field() #服务类型
    taste = scrapy.Field() #口味评分
    service = scrapy.Field() #服务评分
    environment = scrapy.Field() #环境评分

    pass
