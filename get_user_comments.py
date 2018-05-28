#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 16:58
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取用户的评论，通过user_list.csv文件


import re
import sys
import time
import urllib
import urllib2

from BeautifulSoup import BeautifulSoup

import config
from wait import wait_time

reload(sys)
sys.setdefaultencoding("utf8")

user_agent = config.user_agent
cookie = config.cookie
user_list_path=config.user_list_path
comments_path=config.comments_path


def get_comments(user_id):
    """
    获取某个用户的所有评论
    :param user_id:
    :return:
    """
    user_url = "http://www.dianping.com/member/" + str(user_id) + "/reviews"
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
    print page_num

    user_name = soup.find(name="h2", attrs={"class": "name"}).text

    print user_id, user_name, "pages:1" + " " + user_url
    lis = soup.find(name="div", attrs={"class": "pic-txt"}).findAll(name="div", attrs={"class": "txt J_rptlist"})
    get_user_page_comment(lis, user_id, user_name)

    for num in range(2, page_num + 1):
        time.sleep(wait_time(5,2))
        url = user_url + "?pg=" + str(num) + "&reviewCityId=0&reviewShopType=0&c=0&shopTypeIndex=0"
        print user_id, user_name, "pages:" + str(num) + " " + url
        request = urllib2.Request(url, headers=headers)  # 发送网络请求
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response.read())
        lis = soup.find(name="div", attrs={"class": "pic-txt"}).findAll(name="div", attrs={"class": "txt J_rptlist"})
        get_user_page_comment(lis, user_id, user_name)


def get_user_page_comment(lis_soup, user_id, user_name):
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
        with open(comments_path, "a") as f:
            try:
                f.write("\t".join(content))
                f.write("\n")
            except:
                print(content)


def get_all_comments(start_num):
    """
    获取所有评论
    :param start_num: 开始的用户编号
    :return:
    """
    with open(user_list_path, "r") as f:
        users = f.readlines()

    for num in range(start_num, len(users)):
        user = users[num]
        print("user num:", num)
        get_comments(user.strip("\n"))
        time.sleep(wait_time(5,2))


def get_pic(pic_url):
    """
    获取图片
    :param pic_url:
    :return:
    """
    urllib.urlretrieve(pic_url, '%s.jpg' % 1)


def get_some_coments(user_id, page_num, start_num, user_name):
    """
    获取部分评论
    :param user_id: 用户id
    :param page_num: 总共页数
    :param start_num: 开始爬的页码
    :param user_name: 用户名
    :return:
    """
    user_url = "http://www.dianping.com/member/" + str(user_id) + "/reviews"
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
        time.sleep(wait_time(5,2))


if __name__ == '__main__':
    start_num = 0   # 从第几个用户开始，由于所有用户数据都在一个文件里，每次跑时需要修改
    get_all_comments(start_num)
    # get_some_coments("1525049",165,57,"洋葱小姐会开花")
