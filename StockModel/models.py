from django.db import models


# python manage.py migrate   # 创建表结构
# python manage.py makemigrations StockModel  # 让 Django 知道我们在我们的模型有一些变更
# python manage.py migrate StockModel   # 创建表结构


# Create your models here.
# 支撑位股票
class StockZcw(models.Model):
    # 股票代码
    code = models.CharField(max_length=30, unique=True)
    # 交易所
    house = models.CharField(max_length=10,null=True, blank=True,default='')
    # 股票名称
    name = models.CharField(max_length=10,null=True, blank=True,default='')
    # 当前价格
    price = models.FloatField(default=0)
    # 买入价格
    buy_price = models.FloatField(default=0)
    # 止盈价格
    stop_surplus = models.FloatField(default=0)
    # 止损价格
    stop_loss = models.FloatField(default=0)
    # 涨跌幅（百分比）
    zdf = models.FloatField(default=0)
    # 换手率（百分比）
    hsl = models.FloatField(default=0)
    # 市盈率
    syl = models.FloatField(default=0)
    # 市净率
    sjl = models.FloatField(default=0)
    # 总市值
    zsz = models.FloatField(default=0) # 假设总市值可能较大
    # 量比
    lb = models.FloatField(default=0) 
    # 流通市值
    ltsz = models.FloatField(default=0)
    # 创建时间
    create_time = models.DateTimeField(null=True)
    # 更新时间
    update_time = models.DateTimeField(null=True)
    
    
# 股票重大事件机遇表
class stockEvents(models.Model):
    id = models.AutoField(primary_key=True)
    # 股票代码
    code = models.CharField(max_length=30)
    # 事件备注
    event_remark = models.CharField(max_length=1000,null=True, blank=True,default='')
    # 事件时间
    event_time = models.DateTimeField(null=True)
    # 股票开始时间
    start_time = models.DateTimeField(null=True)
    # 股票结束时间
    end_time = models.DateTimeField(null=True)
    # 创建时间
    create_time = models.DateTimeField(null=True)
    # 更新时间
    update_time = models.DateTimeField(null=True)



    
# 行业概念表
class stockConcepts(models.Model):
    id = models.AutoField(primary_key=True)
    # 行业名称
    name = models.CharField(max_length=10,null=True, blank=True,default='')
    # 排序
    sort = models.IntegerField(default=0)
    # 行业名称
    stocks = models.CharField(max_length=10000,null=True, blank=True,default='')
    # 创建时间
    create_time = models.DateTimeField(null=True)
    # 更新时间
    update_time = models.DateTimeField(null=True)
    


# 投资框架
class stockOpportunity(models.Model):
    id = models.AutoField(primary_key=True)
    # 标题
    title = models.CharField(max_length=10,null=True, blank=True,default='')
    # 内容
    text = models.CharField(max_length=1000,null=True, blank=True,default='')
    # 排序
    sort = models.IntegerField(default=0)
    # 更新时间
    update_time = models.DateTimeField(null=True)


# 近年周期股票
class stockCycle(models.Model):
    id = models.AutoField(primary_key=True)
    # 股票代码
    code = models.CharField(max_length=30)
    # 更新时间
    update_time = models.DateTimeField(null=True)

# 我关心的股票
class stockMyCare(models.Model):
    id = models.AutoField(primary_key=True)
    # 股票代码
    code = models.CharField(max_length=30)
    # 更新时间
    update_time = models.DateTimeField(null=True)


