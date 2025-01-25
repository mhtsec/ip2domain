#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

import re
import requests
import json


def Pearrank(domain, timeout):
    try:
        # 更新请求地址和参数
        response = requests.get(
            f"https://api.mir6.com/api/bdqz?domain={domain}&type=json",
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        # 统一使用新的数据结构解析
        return {
            "code": 1,
            "bdpc_rank": data["data"]["baidupc"],
            "bdmb_rank": data["data"]["baidum"],
            "360rank": data["data"]["so360"],
            "sm_rank": data["data"]["shenma"],
            "sg_rank": data["data"]["sougou"],
            # 新增google字段
            "google_rank": data["data"]["google"]
        }
    except Exception as e:
        print(f"请求异常: {e}")
        return {"code": -1}


if __name__ == '__main__':
    rank = Pearrank("aizhan.com", 12)
    print(rank)


def get_pearrank(domain):
    try:
        response = requests.get(f"https://api.mir6.com/api/bdqz?domain={domain}&type=json")
        response.raise_for_status()
        data = response.json()
        
        return {
            'domain': domain,
            'baidu': data['data']['baidupc'],
            'baidu_mobile': data['data']['baidum'],
            '360': data['data']['so360'],
            'shenma': data['data']['shenma'],
            'sogou': data['data']['sougou'],
            'google': data['data']['google'],
            'status': 'success'
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

