#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/8 23:35
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 获取评论涉及到的店铺



def get_shops():
    shops = []
    current_shops=get_current_shops()
    with open("shop_list.csv", "a") as fa:
        with open("comments1.csv", "r") as fr:
            comments = fr.readlines()
            for comment in comments:
                comment_info = comment.strip("\n").split("\t")
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
    获取现有所有用户id
    :return:
    """
    shops = []
    with open("shop_list.csv", "r") as fr:
        for line in fr:
            shops.append(line.strip("\n"))
    return shops

if __name__ == '__main__':
    get_shops()
