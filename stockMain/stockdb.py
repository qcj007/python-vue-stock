# -*- coding: utf-8 -*-
 
from django.http import JsonResponse
from StockModel.models import StockZcw,stockEvents,stockConcepts,stockOpportunity,stockCycle,stockMyCare

from . import views
import json
from rest_framework import serializers
import requests
import akshare as ak
from datetime import datetime
# 组装响应
def makeResponse(data, errcode=0, errmsg=""):
    try:
        json_data = {
            'errcode': errcode,
            'data': data
        }
        # 只有当errmsg是非空字符串时才添加到响应中
        if isinstance(errmsg, str) and errmsg:
            json_data['errmsg'] = errmsg
        return JsonResponse(json_data)
    except Exception as e:
        # 注意：这里为了示例简洁，直接打印异常。实际应用中，应根据项目要求进行错误记录或处理。
        print(f"创建JSON响应时发生错误: {e}")
        # 根据需要，可以考虑返回一个标准错误响应或执行其他错误处理逻辑。
        # 例如，返回一个空响应或包含错误信息的响应。
        return JsonResponse({})


# 查询某一条记录
def searchZcwStockInfo(request):
    try:
        body = json.loads(request.body)
        code_list = body.get("code_list")
        stock_list = StockZcw.objects.filter(code__in=code_list)
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = MyModelSerializer(stock_list, many=True)
        data_list = serializer.data
        return makeResponse(data_list)
    except Exception as e:
        print(f"searchZcwStockInfo错误: {e}")
        return makeResponse("",-1,"股票查询失败")



# 添加支撑位数据
def addZcwStockInfo(stock):
    code=stock['code']
    stockItem = StockZcw.objects.filter(code=code)
    if len(stockItem)>0:
        return False
    else:
        buy_price = stock['buy_price']
        name = stock['name']
        house = stock['house']
        stop_surplus = stock['stop_surplus']
        stop_loss = stock['stop_loss']
        now_time = views.getNowTime()
        dbFun = StockZcw(code=code,house=house,name=name,buy_price=buy_price,stop_surplus=stop_surplus,stop_loss=stop_loss,create_time=now_time,update_time=now_time)
        dbFun.save()
    return True
# ZCW
# 添加数据
def addZcwStocks(request):
    try:
        body = json.loads(request.body)
        stock = body.get("stock")
        res = addZcwStockInfo(stock)
        if res==True:
            return makeResponse("success")
        else:
            return makeResponse("",-1,"股票已存在")
    except Exception as e:
        print(f"addZcwStocks错误: {e}")
        return makeResponse("",-1,"股票保存失败")
    
# 更新股票信息
def editZcwStocks(request):
    try:
        body = json.loads(request.body)
        list =  body.get("list")
        for item in list:
            code= item['code']
            buy_price= item['buy_price']
            stop_surplus= item['stop_surplus']
            stop_loss= item['stop_loss']
            update_time = views.getNowTime()
            # 向supportLevelStocks更新price
            StockZcw.objects.filter(code=code).update(buy_price=buy_price,stop_surplus = stop_surplus,stop_loss=stop_loss,update_time=update_time)
        return makeResponse("success")   
    except Exception as e:
        print(f"editZcwStocks错误: {e}")
        return makeResponse("",-1,"股票更新失败")


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockZcw
        fields = ('id', 'code', 'house', 'name', 'price', 'buy_price', 'stop_surplus', 'stop_loss', 'zdf', 'hsl','lb', 'syl', 'sjl', 'zsz', 'ltsz','create_time','update_time')  # 指定你需要返回的字段


# 查询数据表
def searchZcwList(code_list):
    try:
        data_list=[]
        if code_list=='null':
            objects = StockZcw.objects.all()
            # 使用序列化器将模型实例转换为可序列化的字典列表
            serializer = MyModelSerializer(objects, many=True)
            data_list = serializer.data
        else:
            objects = StockZcw.objects.filter(code__in=code_list)
            serializer = MyModelSerializer(objects, many=True)
            data_list = serializer.data
        return data_list
    except Exception as e:
        print(f"searchZcwStocksList错误: {e}")
        return []


# 查询支撑位列表
def searchZcwStocksList(code_list):
    try:
        data_list=searchZcwList(code_list)
        search_str = ''
        # 循环判断是否需要更新
        for row in data_list:
            update_time = row['update_time']
            price = row['price']
        
            time_obj = views.getTimeStamp(update_time)
            need_upate = time_obj['need_upate']
            if need_upate == True or price==0:
                code= row['code']
                house = row['house']
                search_str+=house.lower()+code+','

        # search_str>0说明需要更新
      
        if len(search_str)>0:
            print("更新股票")
            stockTickList = views.tickprice(search_str)
            now_time = views.getNowTime()
            for stock in stockTickList:
                StockZcw.objects.filter(code=stock.code).update(name=stock.name,lb=stock.lb,price = stock.price,zdf=stock.zdf,hsl=stock.hsl,syl=stock.syl,sjl=stock.sjl,zsz=stock.zsz,ltsz=stock.ltsz,update_time=now_time)

            data_list=searchZcwList(code_list)

        # 返回JSON格式的数据
        return data_list
    except Exception as e:
        print(f"searchZcwStocksList错误: {e}")
        return []
    


"""
    1. 从数据库中查询数据
    2. 使用序列化器将模型实例转换为可序列化的字典列表
    3. 返回序列化后的字典列表
"""

#  用户获取支撑位价值投资股票列表
def searchZcwStocks(request):
    try:
        body = json.loads(request.body)
        code_list = body.get("code_list") or []
        data_list = searchZcwStocksList(code_list)

        # 返回JSON格式的数据
        return makeResponse(data_list)
    except Exception as e:
        print(f"searchZcwStocks错误: {e}")
        return makeResponse("",-1,"股票查询失败")

# 删除股票
def deleteZcwStocks(request):
    try:
        body = json.loads(request.body)
        list =  body.get("list")
        for code in list:
            StockZcw.objects.get(code=code).delete()
        return makeResponse("success")   
    except Exception as e:
        print(f"deleteZcwStocks错误: {e}")
        return makeResponse("",-1,"股票更新失败")
    

# 查询单个股票信息
def searchStockInfo(request):
    body = json.loads(request.body)
    code =  body.get("code")
    try:
        stockItem = views.searchStockInfo(code)
        if stockItem is not None:
            return makeResponse(stockItem) 
        return makeResponse("",-1,f"股票{code}查询失败")
    except Exception as e:
        print(f"searchStockInfo错误: {e}")
        return makeResponse("",-1,f"股票{code}查询失败")
    


class stockEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockEvents
        fields = ('id', 'code',  'event_remark', 'event_time', 'start_time', 'end_time', 'create_time','update_time')  # 指定你需要返回的字段

# 查询股票事件列表
def searchStocksEvents(request):
    try:
        body = json.loads(request.body)
        objects = stockEvents.objects.all()
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = stockEventsSerializer(objects, many=True)
        data_list = serializer.data
        code_list = list(map(lambda obj: obj['code'], data_list))
        zcw_data_list = searchZcwStocksList(code_list)
        # 创建一个空列表来存储结果
        result_array = []
        
        # 遍历数组A
        for item_a in data_list:
            item_a['event_time'] = views.getTimeStamp(item_a['event_time'])['ymd']
            item_a['start_time'] = views.getTimeStamp(item_a['start_time'])['ymd']
            item_a['end_time'] = views.getTimeStamp(item_a['end_time'])['ymd']
            for item_b in zcw_data_list:
                # 如果找到code相同的项
                if item_a['code'] == item_b['code']:
                    if 'id' in item_b:
                        del item_b['id']
                    # 将数组B中匹配项的内容合并到数组A的项中（这里使用了字典更新操作）
                    item_a.update(item_b)
                    # 将更新后的item_a添加到结果数组中
                    # 由于我们只需要找到第一个匹配项，所以在找到后可以跳出内层循环
                    result_array.append(item_a)
                    break

        return makeResponse(result_array)
    except Exception as e:
        print(f"searchMajorEvents错误: {e}")
        return makeResponse("",-1,"股票查询失败")
    

# 新增股票事件
# 添加数据
def addStocksEvents(request):
    try:
        body = json.loads(request.body)
        house = body.get("house")
        code = body.get("code")
        name = body.get("name")
        event_remark = body.get("event_remark")
        event_time = body.get("event_time")
        start_time = body.get("start_time")
        end_time = body.get("end_time")
        now_time = views.getNowTime()
        dbFun = stockEvents(code=code,event_remark=event_remark,event_time=event_time,start_time=start_time,end_time=end_time,create_time=now_time,update_time=now_time)
        dbFun.save()
        return makeResponse("success")
    except Exception as e:
        return makeResponse("",-1,"股票保存失败")
    
# 更新股票信息
def editStocksEvents(request):
    try:
        body = json.loads(request.body)
        id = body['id']
        house = body.get("house")
        code = body.get("code")
        name = body.get("name")
        event_remark = body.get("event_remark")
        event_time = body.get("event_time")
        start_time = body.get("start_time")
        end_time = body.get("end_time")
        now_time = views.getNowTime()
        stockEvents.objects.filter(id=id).update(code=code,event_remark=event_remark,event_time = event_time,start_time=start_time,end_time=end_time,update_time=now_time)
        return makeResponse("success")   
    except Exception as e:
        print(f"editZcwStocks错误: {e}")
        return makeResponse("",-1,"股票更新失败")


# 删除股票
def deleteStocksEvents(request):
    try:
        body = json.loads(request.body)
        id_list =  body.get("list")
        stockEvents.objects.filter(id__in=id_list).delete()
        return makeResponse("success")   
    except Exception as e:
        print(f"deleteZcwStocks错误: {e}")
        return makeResponse("",-1,"股票删除失败")
    

class stockConceptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockConcepts
        fields = ('id', 'name',  'sort', 'stocks', 'create_time','update_time')  # 指定你需要返回的字段
def searchConcepts():
    try:
        objects = stockConcepts.objects.all()
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = stockConceptsSerializer(objects, many=True)
        data_list = serializer.data
        return data_list
    except Exception as e:
        print(f"searchConcepts错误: {e}")
        return []

# 查询行业概念列表
def searchStocksConcepts(request):
    try:
        data_list = searchConcepts()
        return makeResponse(data_list)
    except Exception as e:
        print(f"searchStocksConcepts错误: {e}")
        return makeResponse("",-1,"行业概念查询失败")
    
# 添加行业概念
def addStocksConcepts(request):
    try:
        body = json.loads(request.body)
        name = body.get("name")
        sort = body.get("sort")
        now_time = views.getNowTime()
        dbFun = stockConcepts(name=name,sort=sort,stocks='',create_time=now_time,update_time=now_time)
        dbFun.save()
        data_list = searchConcepts()
        return makeResponse(data_list)
    except Exception as e:
        print(f"addStocksConcepts错误: {e}")
        return makeResponse("",-1,"行业概念保存失败")
    
# 删除行业概念
def deleteStocksConcepts(request):
    try:
        body = json.loads(request.body)
        id = body.get("id")
        stockConcepts.objects.filter(id=id).delete()
        data_list = searchConcepts()
        return makeResponse(data_list) 
    except Exception as e:
        print(f"deleteStocksConcepts错误: {e}")
        return makeResponse("",-1,"行业概念删除失败")

# 更新行业概念
def editStocksConcepts(request):
    try:
        body = json.loads(request.body)
        list = body.get("list")
        now_time = views.getNowTime()
        
        for item in list:
            name=item['name']
            sort=item['sort']
            stocks=item['stocks']
            id=item['id']
            stockConcepts.objects.filter(id=id).update(name=name,sort=sort,stocks=stocks,update_time=now_time)
        return makeResponse("success")   
    except Exception as e:
        print(f"editStocksConcepts错误: {e}")
        return makeResponse("",-1,"行业概念更新失败")
 



class stockOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = stockOpportunity
        fields = ('id', 'title',  'sort', 'text', 'update_time')  # 指定你需要返回的字段


def searchStockOppty():
    try:
        objects = stockOpportunity.objects.all()
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = stockOpportunitySerializer(objects, many=True)
        data_list = serializer.data
        return data_list
    except Exception as e:
        print(f"searchConcepts错误: {e}")
        return []
# 查询投资框架
def searchStockOpportunity(request):
    try:
        data_list = searchStockOppty()
        return makeResponse(data_list)
    except Exception as e:
        print(f"searchStocksConcepts错误: {e}")
        return makeResponse("",-1,"查询投资框架失败")
    
# 添加投资框架
def addStockOpportunity(request):
    try:
        body = json.loads(request.body)
        title = body.get("title")
        text = body.get("text")
        sort = body.get("sort")
        now_time = views.getNowTime()
        dbFun = stockOpportunity(title=title,sort=sort,text=text,update_time=now_time)
        dbFun.save()
        data_list = searchStockOppty()
        return makeResponse(data_list)
    except Exception as e:
        print(f"addStocksConcepts错误: {e}")
        return makeResponse("",-1,"投资框架保存失败")
    
# 删除投资框架
def deleteStockOpportunity(request):
    try:
        body = json.loads(request.body)
        id = body.get("id")
        stockOpportunity.objects.filter(id=id).delete()
        data_list = searchStockOppty()
        return makeResponse(data_list) 
    except Exception as e:
        print(f"deleteStocksConcepts错误: {e}")
        return makeResponse("",-1,"投资框架删除失败")

# 更新投资框架
def editStockOpportunity(request):
    try:
        body = json.loads(request.body)
        list = body.get("list")
        now_time = views.getNowTime()
        
        for item in list:
            title=item['title']
            sort=item['sort']
            text=item['text']
            id=item['id']
            stockOpportunity.objects.filter(id=id).update(title=title,sort=sort,text=text,update_time=now_time)
        return makeResponse("success")   
    except Exception as e:
        print(f"editStocksConcepts错误: {e}")
        return makeResponse("",-1,"投资框架更新失败")
 

# ----------------------周期性股票--------------------

 
class stockCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockCycle
        fields = ('id', 'code',  'update_time')  # 指定你需要返回的字段

# 查询周期股票
def searchStockCycle(request):
    try:
        objects = stockCycle.objects.all()
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = stockCycleSerializer(objects, many=True)
        data_list = serializer.data

        return makeResponse(data_list)
    except Exception as e:
        print(f"searchStockCycle错误: {e}")
        return makeResponse("",-1,"查询周期股票失败")
    
# 添加周期股票
def addStockCycle(request):
    try:
        body = json.loads(request.body)
        code = body.get("code")
        now_time = views.getNowTime()
        dbFun = stockCycle(code=code,update_time=now_time)
        dbFun.save()
        return makeResponse("success")
    except Exception as e:
        print(f"addStockCycle错误: {e}")
        return makeResponse("",-1,"周期股票保存失败")
    
# 删除周期股票
def deleteStockCycle(request):
    try:
        body = json.loads(request.body)
        code = body.get("code")
        stockCycle.objects.filter(code=code).delete()
        return makeResponse("success") 
    except Exception as e:
        print(f"deleteStockCycle错误: {e}")
        return makeResponse("",-1,"周期股票删除失败")



# ----------------------我关注的股票--------------------

class stockMyCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = stockMyCare
        fields = ('id', 'code',  'update_time')  # 指定你需要返回的字段

# 查询我关心的股票
def searchStockMyCare(request):
    try:
        objects = stockMyCare.objects.all()
        # 使用序列化器将模型实例转换为可序列化的字典列表
        serializer = stockMyCareSerializer(objects, many=True)
        data_list = serializer.data

        return makeResponse(data_list)
    except Exception as e:
        print(f"searchStockMyCare错误: {e}")
        return makeResponse("",-1,"查询我关心的股票失败")
    
# 添加我关心的股票
def addStockMyCare(request):
    try:
        body = json.loads(request.body)
        code = body.get("code")
        now_time = views.getNowTime()
        dbFun = stockMyCare(code=code,update_time=now_time)
        dbFun.save()
        return makeResponse("success")
    except Exception as e:
        print(f"addStockMyCare错误: {e}")
        return makeResponse("",-1,"我关心的股票保存失败")
    
# 删除我关心的股票
def deleteStockMyCare(request):
    try:
        body = json.loads(request.body)
        code = body.get("code")
        stockMyCare.objects.filter(code=code).delete()
        return makeResponse("success") 
    except Exception as e:
        print(f"deleteStockMyCare错误: {e}")
        return makeResponse("",-1,"周期我关心的删除失败")

