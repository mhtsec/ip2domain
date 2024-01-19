#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

import re
import requests
import json


def Pearrank(domain, timeout):
    
    reqURL = "https://api.pearktrue.cn/api/website/weight.php?domain="+domain


    baiduRankResult = {"code": 1, "bdpc_rank": -1,"bdmb_rank":-1,"360rank":-1,"sm_rank":-1,"sg_rank":-1}
    try:
        rep = requests.get(url=reqURL, timeout=timeout)
        response = rep.text
        
        start_index = response.find('{')

# 如果找到了左大括号，截取从左大括号开始到字符串结束的部分
        if start_index != -1:
            json_str = response[start_index:]

    # 解析JSON
            try:
                data =json.loads(json_str)
        
       # pc_br_value = data["data"]["success"][0]["pc_br"]
        #m_br_value = data["data"]["success"][0]["m_br"]
                baiduRankRegular = {"code": 1, "bdpc_rank": data["data"]["Baidu_PC"],"bdmb_rank": data["data"]["Baidu_Mobile"],"360rank":data["data"]["360"],"sm_rank": data["data"]["ShenMa"],"sg_rank": data["data"]["SoGou"]}
        

                return baiduRankRegular 
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
        else:
            print("未找到左大括号")


    except:
        
        baiduRankResult["code"] = -1
        return baiduRankResult
    


if __name__ == '__main__':
    rank = Pearrank("aizhan.com", 12)
    print(rank)

