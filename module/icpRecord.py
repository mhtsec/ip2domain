#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

import requests
import json

def searchRecord(domain, timeout):

    resultDic = {"code":1, "domain":domain, "unitName": "None", "unitICP": "None"}
    try:
        rep = requests.get(url=f"https://api.pearktrue.cn/api/icp/?domain="+domain, timeout=timeout)
        response = rep.text
        data =json.loads(response)
        try:
            resultDic["unitName"] = data["data"]["hostingparty"]
        except:
            pass
        try:
            resultDic["unitICP"] = data["data"]["filingnumber"]
        except:
            pass
       
        return resultDic
    except:
        
        return resultDic

if __name__ == "__main__":
    __name__
    
