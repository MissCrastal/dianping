#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/8 23:35
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取评论涉及到的店铺

import os

import config

shop_list_path=config.shop_list_path
comments_path=config.comments_path


def get_shops(start_comment):
    shops = []  # 不重复的记录新增商家
    current_shops=get_current_shops()
    with open(shop_list_path, "a") as fa:
        with open(comments_path, "r") as fr:
            comments = fr.readlines()
            for num in range(start_comment,len(comments)):
                comment_info = comments[num].strip("\n").split("\t")
                shop_id = comment_info[2]
                shop_name = comment_info[3]
                if shop_id in shops or shop_id in current_shops:
                    pass
                else:
                    shops.append(shop_id)
                    try:
                        fa.write("\t".join([shop_id, shop_name]))
                        fa.write("\n")
                    except:
                        print(shop_id)


def get_current_shops():
    """
    获取现有所有商户id
    :return:
    """
    if not os.path.exists(shop_list_path):
        return []
    cur_shops = []
    with open(shop_list_path, "r") as fr:
        for line in fr:
            cur_shops.append(line.strip("\n"))
    return cur_shops

if __name__ == '__main__':
    start_comment=0     # 从第几个评论开始算起，由于所有评论数据都在一个文件里，当评论数据非常多以后，修改起始评论编号可以节约时间
    get_shops(start_comment)
