#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/8 23:55
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : get_shop_info.py

import re
import sys
import time
import urllib2

from BeautifulSoup import BeautifulSoup

import config
from wait import wait_time

reload(sys)
sys.setdefaultencoding("utf8")


user_agent = config.user_agent
cookie = config.cookie
shop_info_path=config.shop_info_path
shop_list_path=config.shop_list_path




def get_shop_info(shop_id):
    """
    获取某个店的信息
    :param shop_id:
    :return:
    """
    shop_url = "http://www.dianping.com/shop/" + str(shop_id)
    headers = {'User-Agent': user_agent, "cookie": cookie}

    print "start_shop:" + shop_id, shop_url

    request = urllib2.Request(shop_url, headers=headers)  # 发送网络请求
    response = urllib2.urlopen(request)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html)
    basic_info = soup.find(name="div", attrs={"id": "basic-info"})
    if not basic_info:
        title = soup.find(name="title")
        if title and title.text == "验证中心":
            print("验证页面，需要输入验证码")
            sys.exit(0)
        else:
            print "商家类型 error"
            return ["商家类型error"]
    address = basic_info.find(name="span", attrs={"itemprop": "street-address"})["title"]
    phone_soup = basic_info.find(name="span", attrs={"itemprop": "tel"})
    if phone_soup:
        phone = phone_soup.text
    else:
        phone = None
    brief_info = basic_info.find(name="div", attrs={"class": "brief-info"})
    # review_count = brief_info.find(name="span", attrs={"id": "reviewCount"}).text       # 评论总数
    # average_price = brief_info.find(name="span", attrs={"id": "avgPriceTitle"}).text    # 人均消费
    # comment_score = brief_info.find(name="span", attrs={"id": "comment_score"})
    # spans = comment_score.findAll(name="span")
    # sweet = spans[0].text       # 口味
    # enviroment = spans[1].text  # 环境
    # service = spans[2].text     # 服务
    score = re.search(r"\d+", brief_info.find(name="span")["class"]).group()
    shop_detail = [address, str(phone), score]
    for span in brief_info.findAll(name="span", attrs={"class": "item"}):
        shop_detail.append(span.text)
    shop_type = soup.find(name="div", attrs={"class": "breadcrumb"}).findAll(name="a")
    for type_data in shop_type:
        shop_detail.append(type_data.text)
    return shop_detail


def get_all_shop_info(start_num):
    """
    获取shop_list.csv文件下所有商户的商户信息
    :param start_num: 开始的商家号
    :return:
    """
    with open(shop_list_path, "r") as fr:
        shops = fr.readlines()
        for num in range(start_num, len(shops)):
            shop_info = shops[num].strip("\n").split("\t")
            shop_id = shop_info[0]
            print("shop num:", num)
            shop_info.extend(get_shop_info(shop_id))
            with open(shop_info_path, "a") as fa:
                fa.write("\t".join(shop_info))
                fa.write("\n")
            wait_seconds = wait_time(3, 2)
            print "sleep:"+str(wait_seconds)
            time.sleep(wait_seconds)


if __name__ == '__main__':
    start_num=2298
    get_all_shop_info(start_num)
    # print(get_shop_info("69734332"))
