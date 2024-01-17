#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

def banner():
    logo = f"""
                  _________
                      |
                      |
                     _|_
                ///\(\033[0m\033[31mo\033[0m\033[92m_\033[0m\033[31mo\033[0m\033[92m)/\\\\\\
                |||  ` '  |||
     ip2domain                24.1.17 棉花糖修复增强版 公众号:棉花糖网络安全圈
                    v1.0
    """
    msg = f"""  ip2domain：IP反查域名，查询备案信息、查询百度权重
            
 (由于接口对请求频率有限制，故查询速率较慢，请耐心等待)
    """
    print("\033[92m" + logo + "\033[0m")
    print(msg)

if __name__ == "__main__":
    pass
