# -*- coding: utf-8 -*-
from scrapy.http import Request
from ..items import DpSpiderItem
from scrapy_redis.spiders import RedisSpider
import redis
import re
from redis import Redis
from scrapy import log
from time import sleep
# ------------------------------------------
#   版本：1.0
#   日期：2018-07-19
#   作者：xishu
# ------------------------------------------




class dpspider(RedisSpider):
    name = 'dpspider'
    redis_key = "dpspider:start_urls"
    page=0
    #allowed_domains = ['dianping.com']
    #start_urls = ['http://zhihu.com/']
    #strat_user_id = ['yun-he-shu-ju-8']
    #动态定义爬虫取域范围
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(dpspider, self).__init__(*args, **kwargs)
    '''
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': 'showNav=#nav-tab|0|0; navCtgScroll=0; navCtgScroll=0; _lxsdk_cuid=16144e1c431c8-0f03606bb8feee-32677403-13c680-16144e1c431c8; _lxsdk=16144e1c431c8-0f03606bb8feee-32677403-13c680-16144e1c431c8; _hc.v=9f575035-6a58-cb21-74aa-0a464ca3d23f.1517279102; cy=3; cye=hangzhou; s_ViewType=10; __mta=248412472.1526355099967.1526355115964.1526355121297.3; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=163625eb540-ef7-508-424%7C%7C168'
            # 'Host': 'cdata.58.com',
            # 'Referer': 'http://webim.58.com/index?p=rb'
        }
        yield Request(self.start_urls[0]+'p%s'%str(self.page+1),headers=headers,method='GET',callback=self.parse)'''

    def parse (self, response):
        shop_lists = response.xpath('//*[@id="shop-all-list"]/ul/li')
        print(response.url)
        if shop_lists==[]:

            redis_url = 'redis://@localhost:6379/'
            r = redis.Redis.from_url(redis_url, decode_responses=True)
            for i in range(int(response.url[-2:].replace('p','')),50):
                d_url=re.sub(r'p$', '', response.url[:-2])+'p%s'%str(i+1)
                r.hdel('dpspider:start_urls',d_url)
            #self.page=0
        else:
            item = DpSpiderItem()
            for shop in shop_lists:
                item["shop_name"]=shop.xpath("./div[2] / div[1] / a[1] / h4 / text()").extract()[0]
                item["shop_url"]=shop.xpath("./div[2] / div[1] / a[1] /@href").extract_first()
                item["menu"] = ';'.join(shop.xpath('./div[@class="txt"]/div[@class="recommend"]/a[@class="recommend-click"]/text()').extract())
                shop_tags=shop.xpath('./div[@class="txt"]/div[@class="tag-addr"]/a[@data-click-name]/span/text()').extract()
                item['shop_kind'] = shop_tags[0]
                item['mall'] = shop_tags[1]
                item['address'] = shop.xpath('./div[@class="txt"]/div[@class="tag-addr"]/span/text()').extract()
                avg_fee=shop.xpath('./div[@class="txt"]/div[@class="comment"]/a[@class="mean-price"]/b/text()').extract()
                if avg_fee==[]:
                    item['avg_fee'] =''
                else:
                    item['avg_fee']=avg_fee[0]
                shop_brand =shop.xpath('./div[@class="txt"]/div[@class="tit"]//a[@class="shop-branch"]/text()').extract()
                if shop_brand==[]:
                    item['shop_brand']=''
                else:
                    item['shop_brand']=shop_brand[0].replace('\n','')
                item['service_type']=' '.join(shop.xpath('./div[@class="txt"]/div[@class="tit"]/div[@class="promo-icon J_promo_icon"]/a[@data-click-name]/@data-click-name').extract())
                comment_list=shop.xpath('./div[@class="txt"]/span[@class="comment-list"]/span/b/text()').extract()
                if comment_list==[]:
                    item['taste']=''
                    item['service']=''
                    item['environment']=''
                else:
                    item['taste']=comment_list[0]
                    item['service'] =comment_list[1]
                    item['environment'] = comment_list[2]
                    '''headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'showNav=#nav-tab|0|0; navCtgScroll=0; navCtgScroll=0; _lxsdk_cuid=16144e1c431c8-0f03606bb8feee-32677403-13c680-16144e1c431c8; _lxsdk=16144e1c431c8-0f03606bb8feee-32677403-13c680-16144e1c431c8; _hc.v=9f575035-6a58-cb21-74aa-0a464ca3d23f.1517279102; cy=3; cye=hangzhou; s_ViewType=10; __mta=248412472.1526355099967.1526355115964.1526355121297.3; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=163625eb540-ef7-508-424%7C%7C168'
        # 'Host': 'cdata.58.com',
        # 'Referer': 'http://webim.58.com/index?p=rb'
         }'''
                #self.page+=1
                #yield Request(re.sub(r'p$', '', response.url[:-2])+'p%s'%str(self.page+1), headers = headers, method = 'GET', callback = self.parse)
                yield item
