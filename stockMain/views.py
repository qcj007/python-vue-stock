from django.http import JsonResponse
import sqlite3
import requests
import json
import akshare as ak
from datetime import datetime,timezone
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


class Tick:
    """ 实时行情数据"""
    code: str  # 股票代码
    name: str  # 股票名称
    price: float  # 当前价格
    zdf: float  # 涨跌幅度
    lb: float   # 量比
    hsl: float  # 换手率
    syl: float  # 市盈率
    sjl: float  # 市净率
    zsz: float  # 总市值
    ltsz: float  # 流通市值
def tickprice(codeString):
    httpString = f"http://qt.gtimg.cn/q={codeString}money.api"
    response = requests.get(httpString).text
    resList = str(response).split(';')
    list = []
    if len(resList)>0:
        for item in resList:
            data = str(item).split('~')
            if len(data)>10:
                tick = Tick()
                tick.price = float(data[3])
                tick.name = data[1]
                tick.code = data[2]
                tick.zdf = data[32]
                tick.hsl = data[38]
                tick.lb = data[49]
                tick.syl = data[39]
                tick.sjl = data[46]
                tick.zsz = data[45]
                tick.ltsz = data[44]
                list.append(tick)
    return list   

# 查询单个股票信息
def searchStockInfo(code):
    try:
        dataList = ak.stock_individual_info_em(symbol=code).to_dict('records')
        stockItem = {}
        if len(dataList)>0:
            for row in dataList:
                stockItem[row["item"]]=row["value"]
        return stockItem
    except Exception as e:
        return None
    


# 事件解析
def getTimeStamp(timestamp_str):
    # 解析时间字符串
    dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

    weekday = dt.weekday()
    # 将数字转换为星期名称
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_name = days_of_week[weekday]
    # 获取小时和分钟
    year = dt.year
    month =f'{dt.month:02}'
    day = f'{dt.day:02}'
    hour = dt.hour
    minute = dt.minute
    # 是否是当天（假设这里的“当天”指的是运行代码时的日期）
    is_today = (dt.date() == datetime.now(timezone.utc).date())
    hour_time = hour + minute/60
    now_timestamp_str=getNowTime()
    now_dt = datetime.fromisoformat(now_timestamp_str.replace("Z", "+00:00"))
    now_hour_time = now_dt.hour + now_dt.minute/60
    
    need_upate = False
    if is_today==False or (weekday<5 and (((now_hour_time>=9.5 and now_hour_time<=11.5) or (now_hour_time>=13 and now_hour_time<=15)) or ((hour_time>=9.5 and hour_time<=11.5) or (hour_time>=13 and hour_time<=15)))):
        need_upate = True
    res = {
        'weekday':weekday,
        'weekday_name':weekday_name,
        'hour':hour,
        'minute':minute,
        'hour_time':hour_time,
        'now_hour_time':now_hour_time,
        'is_today':is_today,
        'ymd':f"{year}-{month}-{day}",
        'need_upate':need_upate
    }

    return res

# 获取当前时间
def getNowTime():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time