#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/8 23:55
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : get_shop_info.py

import re
import sys
import time
import urllib2

import numpy as np
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf8")


def box_muller_sample(mu, sigma):
    '''
    利用Box-Muller生成服从正态分布的随机数
    :param mu: 平均值
    :param sigma: 方差
    :return:
    '''
    u1 = np.random.uniform(size=1)
    u2 = np.random.uniform(size=1)
    R = np.sqrt(-np.log(u1))
    theta = 2 * np.pi * u2
    z = R * np.cos(theta)
    rand_data = mu + z * sigma
    return rand_data[0]


def wait_time(mu, sigma):
    '''
    生成服从正态分布的等待时间，如果小于0则改为1
    :param mu: 平均时间
    :param sigma: 时间方差
    :return:
    '''
    seconds = box_muller_sample(mu, sigma)
    if seconds < 0:
        wait_seconds = 1
    else:
        wait_seconds = seconds
    return wait_seconds


def get_shop_info(shop_id):
    """
    获取某个店的信息
    :param shop_id:
    :return:
    """
    shop_url = "http://www.dianping.com/shop/" + str(shop_id)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=1.2035882514.1519290125.1519290125.1519290125.1; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; cy=16; cye=wuhan; dper=ccab8f9de523d407a93e7aee870d4a21ef006c4334e74709010fb240d070cbca6e57159810f31745f4d8980a12775182c0e740f84990466f9be7cf771b83e000a887166442673ec7d516a4ff6b5d545a27efa8c3aaca5ac2dd2c0f290e15f12a; ua=dpuser_7575831921; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ll=7fd06e815b796be3df069dec7836c3df; __mta=251534265.1525606929473.1525929703867.1525944338404.9; _lxsdk_s=163498e15e4-ee2-020-a87%7C%7C21"
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
    with open("shop_list.csv", "r") as fr:
        shops = fr.readlines()
        for num in range(start_num, len(shops)):
            shop_info = shops[num].strip("\n").split("\t")
            shop_id = shop_info[0]
            print("shop num:", num)
            shop_info.extend(get_shop_info(shop_id))
            with open("shop_info.csv", "a") as fa:
                fa.write("\t".join(shop_info))
                fa.write("\n")
            wait_seconds = wait_time(3, 2)
            print "sleep:"+str(wait_seconds)
            time.sleep(wait_seconds)


if __name__ == '__main__':
    start_num=2298
    get_all_shop_info(start_num)
    # print(get_shop_info("69734332"))
