#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

import time
from argparse import ArgumentParser

def parseArgs():
    date = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", required=False, type=str, help=f"Target ip/domain")
    parser.add_argument("-f", "--file", dest="file", required=False, type=str, default="", help=f"指定目标文件，一行一个，ip或者域名")
    parser.add_argument("-s", "--delay", dest="delay", required=False, type=int, default=2, help=f"请求延迟 (默认 2s)")
    parser.add_argument("-T", "--Timeout", dest="timeout", required=False, type=int, default=12, help="超时时间 (默认 12s)")
    parser.add_argument("-r", "--rank", required=False, type=int, default=0, help="大于指定的百度权重值则输出，范围0-10 (默认 0)")
    parser.add_argument("-o", "--output", dest="output", required=False, type=str, default=f"{date}", help="输出文件 (文件路径： ./output/ip2domain_{fileName}_{date}.csv)")
    parser.add_argument("--icp", required=False, action="store_true", default=False, help="是否开启ICP备案查询 (默认不开启)")
    return parser

if __name__ == "__main__":
    args = parseArgs()

