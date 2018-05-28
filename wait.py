#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2018/5/28 17:10
# @Author   : Edward  Luo<daipeng_luo@qq.com>
# function  : 生成服从正态分布的程序停止时间

import numpy as np

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
