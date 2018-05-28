#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 14:39
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取某件店的所有评论用户, user id会写入到user_list.csv文件中（不重复）

import os
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
user_list_path=config.user_list_path


def get_shop_comment_users(shop_id,start_page):
    """
    获取该店所有的评论用户
    :param shop_id:
    :return:
    """
    review_url = "http://www.dianping.com/shop/" + str(shop_id) + "/review_all"
    headers = {'User-Agent': user_agent, "cookie": cookie}
    request = urllib2.Request(review_url, headers=headers)  # 发送网络请求
    response = urllib2.urlopen(request)
    html = response.read()
    soup = BeautifulSoup(html)
    pages_review = soup.find(name="div", attrs={"class": "reviews-pages"})
    pages = pages_review.findAll(name="a")
    if not pages:
        page_num = 1
    else:
        page_num = int(pages[-2]["data-pg"])
    print("pages:"+str(page_num))

    # file_name = soup.find(name="h1").find(name="a")["title"]
    # print(file_name)
    current_users = get_current_users()

    if start_page==1:
        print("start_page:1", review_url)
        get_usr_id(soup, current_users)
        start_page+=1

    for num in range(start_page, page_num + 1):
        time.sleep(wait_time(5, 2))
        url = review_url + "/p" + str(num)
        print("start_page:"+str(num),url)
        request = urllib2.Request(url, headers=headers)  # 发送网络请求
        response = urllib2.urlopen(request)
        get_usr_id(BeautifulSoup(response.read()), current_users)



def get_usr_id(soup, current_users):
    """
    根据某个评论页面的soup返回所有评论用户的id(和已有用户不重复)
    :param soup:
    :return:
    """
    page_users = []
    items = soup.find(name="div", attrs={"class": "reviews-items"})
    comments = items.findAll(name="a", attrs={"class": "dper-photo-aside"})
    for comment in comments:
        user_id = comment["data-user-id"]
        if user_id in current_users:
            pass
        else:
            page_users.append(comment["data-user-id"])
    with open(user_list_path, "a") as f:
        f.write("\n".join(page_users))
        f.write("\n")


def get_current_users():
    """
    获取现有所有用户id
    :return:
    """
    users = []
    if not os.path.exists(user_list_path):
        return []
    with open(user_list_path, "r") as fr:
        for line in fr:
            users.append(line.strip("\n"))
    return users


if __name__ == '__main__':
    shop_id=76873808
    start_page=1    # 可能前面几页的用户已经抓取过
    get_shop_comment_users(shop_id,start_page)
