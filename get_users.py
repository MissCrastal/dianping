#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 14:39
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取某件店的所有评论用户, user id会写入到user_list.csv文件中（不重复）

import sys
import urllib2
import config
from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf8")


user_agent = config.user_agent
cookie = config.cookie
user_list_path=config.user_list_path


def get_shop_comment_users(shop_id):
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
    print(page_num)

    # file_name = soup.find(name="h1").find(name="a")["title"]
    # print(file_name)
    current_users = get_current_users()

    user_ids = []
    user_ids.extend(get_usr_id(soup, current_users))

    for num in range(2, page_num + 1):
        url = review_url + "/p" + str(num)
        request = urllib2.Request(url, headers=headers)  # 发送网络请求
        response = urllib2.urlopen(request)
        user_ids.extend(get_usr_id(BeautifulSoup(response.read()), current_users))
    print(user_ids)

    with open(user_list_path, "a") as f:
        f.write("\n".join(user_ids))


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
    return page_users


def get_current_users():
    """
    获取现有所有用户id
    :return:
    """
    users = []
    with open(user_list_path, "r") as fr:
        for line in fr:
            users.append(line.strip("\n"))
    return users


if __name__ == '__main__':
    shop_id=11111
    get_shop_comment_users(shop_id)
