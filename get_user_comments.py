#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 16:58
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取用户的评论，通过user_list.csv文件


import re
import sys
import urllib
import urllib2
import time

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


def get_comments(user_id, write_file_path):
    """
    获取某个用户的所有评论
    :param user_id:
    :return:
    """
    user_url = "http://www.dianping.com/member/" + str(user_id) + "/reviews"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=1.2035882514.1519290125.1519290125.1519290125.1; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; __mta=251534265.1525606929473.1525606929473.1525606929473.1; cy=16; cye=wuhan; ctu=b2aaa0d29e0d897feeacb6c72b3e78f09734d34fb1a72bc2745611c6b680ca72bff40589d28aae78fa3c997146cf48d2; dper=ccab8f9de523d407a93e7aee870d4a21ef006c4334e74709010fb240d070cbca6e57159810f31745f4d8980a12775182c0e740f84990466f9be7cf771b83e000a887166442673ec7d516a4ff6b5d545a27efa8c3aaca5ac2dd2c0f290e15f12a; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_7575831921; uamo=17671442006; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1633ad5e724-052-6d5-e14%7C%7C86"
    headers = {'User-Agent': user_agent, "cookie": cookie}

    print "start_user:" + user_id, user_url

    request = urllib2.Request(user_url, headers=headers)  # 发送网络请求
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html)
    pages_item = soup.find(name="div", attrs={"class": "pages-num"})
    if not pages_item:
        page_num = 1
    else:
        pages = pages_item.findAll(name="a")
        page_num = int(pages[-2]["data-pg"])
    print(page_num)

    user_name = soup.find(name="h2", attrs={"class": "name"}).text

    lis = soup.find(name="div", attrs={"class": "pic-txt"}).findAll(name="div", attrs={"class": "txt J_rptlist"})
    get_user_page_comment(lis, user_id, user_name, write_file_path)

    for num in range(2, page_num + 1):
        wait_seconds = box_muller_sample(5, 2)
        time.sleep(wait_seconds)
        url = user_url + "?pg=" + str(num) + "&reviewCityId=0&reviewShopType=0&c=0&shopTypeIndex=0"
        print user_id, user_name, "pages:" + str(num) + " " + url
        request = urllib2.Request(url, headers=headers)  # 发送网络请求
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        lis = soup.find(name="div", attrs={"class": "pic-txt"}).findAll(name="div", attrs={"class": "txt J_rptlist"})
        get_user_page_comment(lis, user_id, user_name, write_file_path)


def get_user_page_comment(lis_soup, user_id, user_name, write_file_path):
    """
    获取某个页面用户的所有评论
    :param lis_soup:
    :param user_id:
    :param user_name:
    :return:
    """
    for li in lis_soup:
        if not li:
            continue
        shop = li.find(name="h6").find("a")
        shop_id = re.sub(r"http.+/", "", shop["href"])
        shop_name = shop.text
        address = li.find(name="div", attrs={"class": "mode-tc addres"}).text
        score_soup = li.find(name="div", attrs={"class": "mode-tc comm-rst"}).find("span")
        if score_soup:
            attr = score_soup.attrs
            if attr and "class" in attr[0]:
                score = re.search(r"\d+", score_soup["class"]).group()
            else:
                score = None
        else:
            score = None
        comment = li.find(name="div", attrs={"class": "mode-tc comm-entry"}).text
        pic_soup = li.find(name="div", attrs={"class": "mode-tc comm-photo"})
        if pic_soup:
            pic_num = re.sub(r"&raquo", "", pic_soup.text)
        else:
            pic_num = "0"
        date = li.find(name="span", attrs={"class": "col-exp"}).text
        content = [str(user_id), user_name, shop_id, shop_name, address, str(score), comment, str(pic_num), date]
        with open(write_file_path, "a") as f:
            try:
                f.write("\t".join(content))
                f.write("\n")
            except:
                print(content)


def get_all_comments(start_num, write_file_path):
    with open("user_list.csv", "r") as f:
        users = f.readlines()
        for num in range(start_num, len(users)):
            user = users[num]
            print("user num:", num)
            get_comments(user.strip("\n"), write_file_path)
            wait_seconds = box_muller_sample(5, 2)
            time.sleep(wait_seconds)


def get_pic(pic_url):
    urllib.urlretrieve(pic_url, '%s.jpg' % 1)


def get_some_coments(user_id, page_num, start_num, user_name):
    user_url = "http://www.dianping.com/member/" + str(user_id) + "/reviews"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=1.2035882514.1519290125.1519290125.1519290125.1; cityInfo=%7B%22cityId%22%3A1%2C%22cityEnName%22%3A%22shanghai%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%22%7D; __mta=251534265.1525606929473.1525606929473.1525606929473.1; cy=16; cye=wuhan; ctu=b2aaa0d29e0d897feeacb6c72b3e78f09734d34fb1a72bc2745611c6b680ca72bff40589d28aae78fa3c997146cf48d2; dper=ccab8f9de523d407a93e7aee870d4a21ef006c4334e74709010fb240d070cbca6e57159810f31745f4d8980a12775182c0e740f84990466f9be7cf771b83e000a887166442673ec7d516a4ff6b5d545a27efa8c3aaca5ac2dd2c0f290e15f12a; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_7575831921; uamo=17671442006; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=1633ad5e724-052-6d5-e14%7C%7C86"
    headers = {'User-Agent': user_agent, "cookie": cookie}

    print "start_user:" + user_id, user_url

    for num in range(start_num, page_num + 1):
        url = user_url + "?pg=" + str(num) + "&reviewCityId=0&reviewShopType=0&c=0&shopTypeIndex=0"
        print user_id, user_name, "pages:" + str(num) + " " + url
        request = urllib2.Request(url, headers=headers)  # 发送网络请求
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        lis = soup.find(name="div", attrs={"class": "pic-txt"}).findAll(name="div", attrs={"class": "txt J_rptlist"})
        get_user_page_comment(lis, user_id, user_name)
        wait_seconds = box_muller_sample(5, 2)
        time.sleep(wait_seconds)


if __name__ == '__main__':
    start_num = 521
    write_file_path = "comment.csv"
    get_all_comments(start_num, write_file_path)
    # get_some_coments("1525049",165,57,"洋葱小姐会开花")
