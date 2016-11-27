# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: kevin
@license: Apache Licence 
@contact: liujiezhang@bupt.edu.cn
@site: 
@software: PyCharm Community Edition
@file: detail.py
@time: 16/11/25 上午10:57
"""

from myfunc import *
from scrapy.http import HtmlResponse
from collections import defaultdict
import itertools
import time
import re
import chardet


def goodsUrlList(home_url):
    '''
    根据三级目录商品首页获取所有详情页url
    :param home_url: http://www.vipmro.com/search/?&categoryId=501110
    :return:url列表
    '''
    # 网站基址
    base = u'http://www.runlian365.com'
    # 所有条件下的列表
    all_group_list = parse(home_url)
    # 保存所有goods的详情页url
    url_list = []
    for url in all_group_list:
        # url = 'http://www.vipmro.com/search/?ram=0.9551325197768372&categoryId=501110&attrValueIds=509805,509801,509806,509807'
        # 解析html
        home_page = getHtml(url)
        html = HtmlResponse(url=url,body=str(home_page))
        urls = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[1]/div/div/h4/a/@href').extract()
        url_list.extend(urls)
    for x in xrange(0,len(url_list)):
        url_list[x] = base + url_list[x]
        print str(x) + url_list[x] 


    #     print(len(urls))
    #     print(urls)
    #     exit()
    # print(len(url_list))
    # print(url_list)
    return url_list

def goodsDetail(detail_url):
    '''
    利用xpath解析关键字段
    :param detail_url: 详情页url
    :return: 各个字段信息 dict
    '''
    goods_data = defaultdict()
    # 详情页链接
    goods_data['source_url'] = detail_url
    # 解析html body必须是str类型
    body = getHtml(detail_url)
    html = HtmlResponse(url=detail_url,body=str(body))
    # 名称
    goods_data['name'] = html.xpath('/html/body/div[4]/div[2]/div/h1/a/text()').extract()[0]
    # 价格(为毛啊1.sub函数第二个参数设置为空输出就没了2.对价格做个lstrip()输出又没了)
    goods_data['price'] = re.sub(ur'^.{3}',' ',html.selector.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/div[1]/p[1]/b/text()').extract()[0]).replace(' ','')
    # 型号
    table = html.selector.xpath('/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]/table').extract()[0]
    goods_data['type'] = re.sub(ur'^.{3}','',html.selector.xpath('/html/body/div[4]/div[2]/div/div[1]/div[2]/div[1]/p[2]/span[1]/font[2]/text()').extract()[0],count = 1)
    # 详情
    goods_data['detail'] = html.selector.xpath('/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div[1]/div/div/div[1]').extract()[0]
    print goods_data['detail']
    # 图片
    goods_data['pics'] = html.selector.xpath('//*[@id="proSmallImg"]').xpath('@src').extract()[0].replace('../','http://www.runlian365.com/')
    goods_data['storage'] = ''
    goods_data['lack_period'] = ''
    goods_data['created'] = int(time.time())
    goods_data['updated'] = int(time.time())

    # print(goods_data['detail'])
    return goods_data

def parse(url):
    '''
    解析url下页面各种选择项组合的url
    :param url: http://www.vipmro.com/search/?&categoryId=501110
    :return:['http://www.vipmro.com/search/?categoryId=501110&attrValueIds=509801,512680,509807,509823']
    '''
    # 解析html
    home_page = getHtml(url)
    html = HtmlResponse(url=url,body=str(home_page))
    #总页数
    page_total = 1
    #三级列表下所有
    url_list = []
    if html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[@class = "pages_next"]'):
        page_total = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()-1]/text()').extract()[0].replace('...','')
    elif html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()]/text()'):
        page_total = html.selector.xpath('/html/body/div[5]/div/div[2]/div/div[2]/div/a[last()]/text()').extract()[0]
    for x in xrange(1,int(page_total)+1):
        url_list.append(url.replace('.html','-'+ str(x) + '.html'))
    return url_list

if __name__ == '__main__':
    # url = 'http://www.vipmro.com/product/587879'
    url = 'http://www.runlian365.com/product/382.html'
    goodsUrlList(url)

