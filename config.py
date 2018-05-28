#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/28 16:34
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : config.py.py

import os
import sys

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; cy=16; cye=wuhan; __mta=251534265.1525606929473.1525929703867.1525944338404.9; ll=7fd06e815b796be3df069dec7836c3df; dper=914e3f802cc8a9cd248546cea4eeaf4ae9516702a0896f191be416fd1a5ccb7f770f48fee0348564d7575786f513474dbc8afaa52d92f2aeb1ffca0bd4e190117b0d0d25bc20cbdfd6351b35655a80dbe610fc3d83304eee631474c9a2be69a9; ua=MissCrastal; uamo=18202753495; cityid=16; msource=default; default_ab=shop%3AA%3A1"

data_path=os.path.join(sys.path[0],"data")
if os.path.exists(data_path):
    pass
else:
    os.mkdir(data_path)

user_list_path=os.path.join(data_path,"user_list.csv")
shop_info_path=os.path.join(data_path,"shop_info.csv")
shop_list_path=os.path.join(data_path,"shop_list.csv")
comments_path=os.path.join(data_path,"comments.csv")
