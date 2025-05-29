# 从django.urls导入path函数
from django.urls import path

# 从当前模块导入视图函数
from . import views,stockdb
from django.views.generic.base import TemplateView  # 1、增加该行
from django.contrib import admin
# 定义URL模式列表，每个模式都映射到一个视图函数
urlpatterns = [
    # path('', views.index),
    path('admin/', admin.site.urls),
    path(r'',TemplateView.as_view(template_name='index.html')),  #2、 增加该行
    path('api/searchZcwStocks', stockdb.searchZcwStocks),
    path('api/editZcwStocks', stockdb.editZcwStocks),
    path('api/deleteZcwStocks', stockdb.deleteZcwStocks),
    path('api/addZcwStocks', stockdb.addZcwStocks),
    path('api/searchZcwStockInfo', stockdb.searchZcwStockInfo),
    path('api/searchStockInfo', stockdb.searchStockInfo),
    path('api/searchStocksEvents', stockdb.searchStocksEvents),
    path('api/editStocksEvents', stockdb.editStocksEvents),
    path('api/deleteStocksEvents', stockdb.deleteStocksEvents),
    path('api/addStocksEvents', stockdb.addStocksEvents),

    path('api/searchStocksConcepts', stockdb.searchStocksConcepts),
    path('api/addStocksConcepts', stockdb.addStocksConcepts),
    path('api/deleteStocksConcepts', stockdb.deleteStocksConcepts),
    path('api/editStocksConcepts', stockdb.editStocksConcepts),
    
    path('api/searchStockOpportunity', stockdb.searchStockOpportunity),
    path('api/addStockOpportunity', stockdb.addStockOpportunity),
    path('api/deleteStockOpportunity', stockdb.deleteStockOpportunity),
    path('api/editStockOpportunity', stockdb.editStockOpportunity),

    path('api/searchStockCycle', stockdb.searchStockCycle),
    path('api/addStockCycle', stockdb.addStockCycle),
    path('api/deleteStockCycle', stockdb.deleteStockCycle),

    path('api/searchStockMyCare', stockdb.searchStockMyCare),
    path('api/addStockMyCare', stockdb.addStockMyCare),
    path('api/deleteStockMyCare', stockdb.deleteStockMyCare),
]


