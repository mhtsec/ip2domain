#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author : mhtsec
# @Github : https://github.com/mhtsec

import os
import re
import csv
import time
import requests
import tldextract
from module.banner import banner
from module.argParse import parseArgs
from module.Pearrank import Pearrank
from module.icpRecord import searchRecord
from module.searchDomain import searchDomain

from colorama import init

init(autoreset=True)

from wcwidth import wcswidth as ww


def rpad(s, n, c=" "):
    # 新增：过滤ANSI颜色代码后再计算显示宽度
    clean_str = re.sub(r'\033\[[\d;]*m', '', s)
    return s + (n - ww(clean_str)) * c


requests.packages.urllib3.disable_warnings()  # 抑制https错误信息


def init(parseClass):
    args = parseClass.parse_args()
    if not args.file and not args.target:
        print(parseClass.print_usage())
        exit(0)

    if args.file:
        if not os.path.isfile(args.file):
            print(
                f"\n[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[31m[ERRO] - Load file [{args.file}] Failed\033[0m")
            exit(0)

    targetList = loadTarget(args.file, args.target)  # 所有目标

    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Timeout:   {args.timeout}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Delay:     {args.delay}s\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - Rank Size: >{args.rank}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ICP:       {args.icp}\033[0m")
    print(
        f"[\033[36m{time.strftime('%H:%M:%S', time.localtime())}\033[0m] - \033[36m[INFO] - ipCount:   {len(targetList)}\033[0m\n")

    return targetList


# 加载目标
def loadTarget(file, target):
    targetList = []

    # 解析输入目标数据
    def parseData(data):
        val = tldextract.extract(data)
        if not val.suffix:
            # 校验解析的数据
            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                        val.domain):
                return f"{val.domain}"
            else:
                return ""
        else:
            return f"{val.domain}.{val.suffix}"

    if file:
        f = open(file, encoding="utf8")
        for line in f.readlines():
            target_ = parseData(line.strip())
            if target_:
                targetList.append(target_)
        f.close()

    if target:
        target_ = parseData(target.strip())
        if target_:
            targetList.append(target_)

    return list(set(targetList))


def outputResult(argsFile, argsOutput, resultList, icp):
    fileName = list(os.path.splitext(os.path.basename(argsFile)))[0]
    outputFile = f"./output/{fileName}_{argsOutput}.csv"
    if not os.path.isdir(r"./output"):
        os.mkdir(r"./output")
    with open(outputFile, "a", encoding="gbk", newline="") as f:
        csvWrite = csv.writer(f)
        if icp:
            csvWrite.writerow(["ip", "反查域名", "百度PC权重", "百度移动权重", "360权重", "神马权重", "搜狗权重", "Google权重", "单位名称", "备案编号"])
        else:
            csvWrite.writerow(["ip", "反查域名", "百度PC权重", "百度移动权重", "360权重", "神马权重", "搜狗权重", "Google权重"])
        
        for result in resultList:
            # 简化转换逻辑，直接写入字符串值
            try:
                # 确保结果有足够的列（包含新增的google排名）
                if len(result) < 8:  # 原有7列 + 新增1列
                    result += ["N/A"]*(8 - len(result))
                csvWrite.writerow(result[:8] + (result[8:] if icp else []))
            except Exception as e:
                print(f"写入错误: {e}")


def ip2domian(target, args, targetNum, targetCount):
    resultList = []
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", target):
        time.sleep(args.delay)
        searchDomainResult = searchDomain(target, args.timeout)
        
        domainList = searchDomainResult["domainList"]
    else:
        domainList = [target]

    for domain in domainList:
        time.sleep(args.delay)
        
        # 修改后的Pearrank结果处理逻辑
        try:
            PearrankResult = Pearrank(domain=domain, timeout=args.timeout) if args.model in [1, 2] else {}
            
            if PearrankResult.get("code") == 1:
                # 统一处理所有排名字段，使用get方法避免KeyError
                ranks = [
                    PearrankResult.get("bdpc_rank", "N/A"),
                    PearrankResult.get("bdmb_rank", "N/A"),
                    PearrankResult.get("360rank", "N/A"),
                    PearrankResult.get("sm_rank", "N/A"),
                    PearrankResult.get("sg_rank", "N/A"),
                    PearrankResult.get("google_rank", "N/A")  # 新增的google排名
                ]
                # 转换数字类型的排名
                ranks = [str(r) if isinstance(r, int) else r for r in ranks]
                resultList.append([target, domain] + ranks)
            else:
                # 全部排名字段标记为错误
                resultList.append([target, domain] + ["Error"]*6)
                
        except Exception as e:
            resultList.append([target, domain] + ["Error"]*6)

    if args.icp:
        for result in resultList:
            icpResult = searchRecord(domain=result[1], timeout=args.timeout)
            time.sleep(args.delay)
            if icpResult["code"] == 1:
                result += [icpResult["unitName"], icpResult["unitICP"]]
            
    if len(resultList) == 0:
        print(f"\r({targetNum}/{targetCount})", end="", flush=True)

    return resultList


def printTitle(icp):
    headers = [
        ("ip/domain", 17),
        ("反查域名", 20),
        ("百度PC", 10),
        ("百度移动", 10),
        ("360", 8),
        ("神马", 8),
        ("搜狗", 8),
        ("Google", 8)
    ]
    
    if icp:
        headers += [("单位名称", 30), ("备案编号", 24)]
    
    # 生成分隔线
    separator = "+".join(["-" * width for _, width in headers])
    print(f"+{separator}+")
    
    # 生成标题行
    title_row = "|".join([rpad(name, width) for name, width in headers])
    print(f"|{title_row}|")
    
    # 生成底部线
    print(f"+{separator}+")


def printMsg(result, icp):
    try:
        COLOR_RED = "\033[31m"
        COLOR_GREEN = "\033[32m"
        COLOR_RESET = "\033[0m"
        
        def is_valid(value):
            # 有效性判断增强：包含None的情况
            if value in [None, "Error", "N/A"]:
                return False
            return str(value).isdigit()
        
        def format_field(value, width):
            # 处理None值
            value = value if value is not None else "Error"
            color = COLOR_GREEN if is_valid(value) else COLOR_RED
            value_str = str(value)[:width//2]  # 防止超长内容破坏格式
            return f"{color}{value_str.center(width)}{COLOR_RESET}"

        # 基础字段优化（调整格式）
        fields = [
            f"{COLOR_GREEN}{result[0][:15].ljust(17)}{COLOR_RESET}",
            f"{COLOR_GREEN}{result[1][:18].ljust(20)}{COLOR_RESET}",
            format_field(result[2], 8),  # 宽度保持10列
            format_field(result[3], 8),
            format_field(result[4], 6),
            format_field(result[5], 6),
            format_field(result[6], 6),
            format_field(result[7], 6)
        ]

        if icp and len(result) >= 9:
            # 单位名称颜色处理
            unit_name = result[8] or "N/A"
            unit_color = COLOR_GREEN if unit_name not in ["N/A", ""] else COLOR_RED
            fields.append(f"{unit_color}{rpad(unit_name, 30)}{COLOR_RESET}")
            
            # 备案编号颜色处理
            icp_value = result[9] if len(result) > 9 else "N/A"
            icp_color = COLOR_GREEN if icp_value not in ["N/A", ""] else COLOR_RED
            fields.append(f"{icp_color}{rpad(str(icp_value)[:24], 24)}{COLOR_RESET}")
        
        # 动态生成分隔线（保持不变）
        col_widths = [17, 20, 10, 10, 8, 8, 8, 8]
        if icp:
            col_widths += [30, 24]
        separator = "+".join(["-" * w for w in col_widths])
        
        # 构建输出行（保持不变）
        output = "|".join([
            rpad(field, width) 
            for field, width in zip(fields, col_widths)
        ])
        
        print(f"\r|{output}|")
        print(f"+{separator}+")
              
    except Exception as e:
        print(f"\n输出错误: {str(e)}")

if __name__ == "__main__":
    banner()
    parseClass = parseArgs()
    args = parseClass.parse_args()
    targetList = init(parseClass)
    resultList = []
    printTitle(args.icp)
    targetCount = len(targetList)
    try:
        for i in range(len(targetList)):
            resultTmpList = []
            resultTmpList += ip2domian(targetList[i], args, targetNum=i+1, targetCount=targetCount)
            resultList += resultTmpList
            for i in resultTmpList:
                printMsg(i, args.icp)
                
        outputResult(args.file, args.output, resultList, args.icp)
            
    except KeyboardInterrupt:
    # 捕获异常，并将异常信息赋值给变量e
        pass
