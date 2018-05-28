#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/6 14:39
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取某件店的所有评论用户, user id会写入到user_list.csv文件中（不重复）

import sys
import urllib2

from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf8")


def get_shop_comment_users(shop_id):
    """
    获取该店所有的评论用户
    :param shop_id:
    :return:
    """
    review_url = "http://www.dianping.com/shop/" + str(shop_id) + "/review_all"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; uamo=18202753495; ua=18202753495; ctu=b2aaa0d29e0d897feeacb6c72b3e78f060e5c7e06ae54ae4d8c4efd0ce27cbb8d049cd7c3151665b938afe2bfc0c0d7f; cy=27; cye=handan; __utmc=1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmb=1.3.10.1525593655; dper=1d870ad6e4b3d5637c542a620c776a71569b41867be0897ea2672f9c1fd0049c; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dsogou.com%26utm_medium%3Dreferral%26utm_content%3D%252Flink; _lxsdk_s=163340ab210-2f3-57d-8c0%7C%7C1384"
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

    with open("user_list.csv", "w") as f:
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
    with open("user_list.csv", "r") as fr:
        for line in fr:
            users.append(line.strip("\n"))
    return users


if __name__ == '__main__':
    shop_id=11111
    get_shop_comment_users(shop_id)
