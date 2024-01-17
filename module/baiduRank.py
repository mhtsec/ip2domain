import re
import requests
import json


def baiduRank(domain, timeout):
    
    reqURL = "https://api.pearktrue.cn/api/website/weight.php?domain="+domain


    baiduRankResult = {"code": 1, "bdpc_rank": -1,"bdmb_rank":-1,"sm_rank":-1,"sg_rank":-1}
    try:
        rep = requests.get(url=reqURL, timeout=timeout)
        response = rep.text
        
        data =json.loads(response)
        
       # pc_br_value = data["data"]["success"][0]["pc_br"]
        #m_br_value = data["data"]["success"][0]["m_br"]
        baiduRankRegular = {"code": 1, "bdpc_rank": int(data["data"]["Baidu_PC"]),"bdmb_rank": int(data["data"]["Baidu_Mobile"]),"sm_rank": int(data["data"]["ShenMa"]),"sg_rank": int(data["data"]["SoGou"])}
        

        return baiduRankRegular 

    except:
        
        baiduRankResult["code"] = -1
        return baiduRankResult
    


if __name__ == '__main__':
    rank = baiduRank("fer.cn", 3)
    print(rank["rank"])

