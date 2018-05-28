#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/28 16:34
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : config.py.py

import os
import sys

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
cookie = "s_ViewType=10; _lxsdk_cuid=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _lxsdk=161bc8b0867c8-0936b88c27d08-4323461-100200-161bc8b0867c8; _hc.v=2b3536d6-3ea5-2c71-6b24-6b2194328e11.1519286684; aburl=1; __utma=1.2035882514.1519290125.1519290125.1519290125.1; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ctu=91412a608d02e58385b163ced37baf6af7b5cfa062bdc424bf3021d541754400; __utmz=1.1519290125.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=1.2035882514.1519290125.1519290125.1519290125.1; cy=16; cye=wuhan; dper=ccab8f9de523d407a93e7aee870d4a21ef006c4334e74709010fb240d070cbca6e57159810f31745f4d8980a12775182c0e740f84990466f9be7cf771b83e000a887166442673ec7d516a4ff6b5d545a27efa8c3aaca5ac2dd2c0f290e15f12a; ua=dpuser_7575831921; __mta=251534265.1525606929473.1525929703867.1525944338404.9; ll=7fd06e815b796be3df069dec7836c3df"

user_list_path=os.path.join(sys.path[0],"data","user_list.csv")
shop_info_path=os.path.join(sys.path[0],"data","shop_info.csv")
shop_list_path=os.path.join(sys.path[0],"data","shop_list.csv")
comments_path=os.path.join(sys.path[0],"data","comments.csv")
