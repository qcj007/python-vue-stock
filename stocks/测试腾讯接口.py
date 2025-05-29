from django.http import JsonResponse
import sqlite3
import requests
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
                print(data[49])
                tick = Tick()
                tick.price = float(data[3])
                tick.name = data[1]
                tick.code = data[2]
                tick.lb = data[49]
                tick.zdf = data[32]
                tick.hsl = data[38]
                tick.syl = data[39]
                tick.sjl = data[46]
                tick.zsz = data[45]
                tick.ltsz = data[44]
                list.append(tick)
    return list   

res = tickprice("sh600570,")
print("res-----",res)