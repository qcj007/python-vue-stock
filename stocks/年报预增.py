import requests
import json
import pandas as pd
import os
import sqlite3



# 判断表是否存在
def table_exists(db_connection, table_name):
    cursor = db_connection.cursor()
    
    # 查询sqlite_master表来确定给定的表名是否存在
    cursor.execute("""
        SELECT COUNT(*) 
        FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (table_name,))
    
    count = cursor.fetchone()[0]
    return count > 0



def get_data(number):
    headers = {
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Cookie":"other_uid=Ths_iwencai_Xuangu_apd7tekcuqcbonye184galxj46uvlru7; ta_random_userid=r091hebdn5; cid=7eb4a1ce12d33fb95712d3b6d40a28f61708602596; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=XCza3sReJt1pPrQcM3cuyUAfj%2ByC%2BsgnxqF3dl8iofNsRbHiabA5eT5tCBMhMaF%2F%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D; u_did=10BAA38E546C4B549FA1008EA2A512B3; u_ttype=WEB; user=MDptb18yNzA5NjczOTc6Ok5vbmU6NTAwOjI4MDk2NzM5Nzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjI3MDk2NzM5NzoxNzEwMDc5NTIzOjo6MTQzNDY0MjMwMDoyNjc4NDAwOjA6MTlmYzdlMTJjODRlN2M1ZmNiNDMwNTY0OTRhMzUxYThlOmRlZmF1bHRfNDox; userid=270967397; u_name=mo_270967397; escapename=mo_270967397; ticket=d17600e8a30d91fa1806c7c84713627c; user_status=0; utk=93305352cae3aa3b32859fa6bf800b78; v=A5Vx4h1UXCJkYnjebk2tkzhYpJpKkk4-E0ct-Bc6UphbTruE3-JZdKOWPdKk"
    }

    data = f"query=%E5%B9%B4%E6%8A%A5%E9%A2%84%E5%A2%9E&urp_sort_way=desc&urp_sort_index=%E9%A2%84%E5%91%8A%E5%87%80%E5%88%A9%E6%B6%A6%E5%8F%98%E5%8A%A8%E5%B9%85%E5%BA%A6%5B20231231%5D&page={number}&perpage=100&addheaderindexes=&condition=%5B%7B%22dateText%22%3A%22%E5%B9%B4%E6%8A%A5%22%2C%22indexName%22%3A%22%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%2C%22indexProperties%22%3A%5B%22%E8%B5%B7%E5%A7%8B%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231231%22%2C%22%E6%88%AA%E6%AD%A2%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231231%22%2C%22%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%3E-%3C%E6%89%AD%E4%BA%8F%3E-%3C%E9%A2%84%E5%A2%9E%22%5D%2C%22dateUnit%22%3A%22%E5%B9%B4%22%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E8%B5%B7%E5%A7%8B%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231231%22%2C%22%E6%88%AA%E6%AD%A2%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231231%22%2C%22%E5%8C%85%E5%90%AB%22%3A%22%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%3E-%3C%E6%89%AD%E4%BA%8F%3E-%3C%E9%A2%84%E5%A2%9E%22%7D%2C%22reportType%22%3A%22FUTURE_QUARTER%22%2C%22dateType%22%3A%22%E6%8A%A5%E5%91%8A%E6%9C%9F%22%2C%22chunkedResult%22%3A%22%E5%B9%B4%E6%8A%A5%E9%A2%84%E5%A2%9E%22%2C%22valueType%22%3A%22_%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_%E8%82%A1%E7%A5%A8%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%B9%B4%E6%8A%A5%E7%9A%84%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%7C%E6%89%AD%E4%BA%8F%7C%E9%A2%84%E5%A2%9E%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%B9%B4%E6%8A%A5%E7%9A%84%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%7C%E6%89%AD%E4%BA%8F%7C%E9%A2%84%E5%A2%9E%22%2C%22relatedSize%22%3A0%2C%22tag%22%3A%22%5B%E5%B9%B4%E6%8A%A5%5D%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%7D%5D&codelist=&indexnamelimit=&logid=33355461f6d81c4c095271354f8b7a10&ret=json_all&sessionid=33355461f6d81c4c095271354f8b7a10&source=Ths_iwencai_Xuangu&date_range%5B0%5D=20231231&date_range%5B1%5D=20231231&iwc_token=0ac9664917106828099447570&urp_use_sort=1&user_id=270967397&uuids%5B0%5D=24087&query_type=stock&comp_id=6836372&business_cat=soniu&uuid=24087"
    url = "https://www.iwencai.com/gateway/urp/v7/landing/getDataList"
    res = requests.post(url, headers=headers, data=data)
    # # res.encoding = "utf-8"
    print(res.status_code)

    json_data = res.json()  # 解析JSON数据
    result = json_data.get("answer")['components'][0]['data']['datas']

    # stockFile = open('movies.json', 'w', encoding='utf-8')
    # stockFile.write(f'{json.dumps(result)}')
    return result

def writeInDb(list):
    # 连接数据库或创建新数据库
    conn = sqlite3.connect("assets/stockDataBase.db")
    # 创建游标
    cursor = conn.cursor()
    

    if table_exists(conn, "profitAddStocks"):
        # 清空profitAddStocks表
        # cursor.execute("DELETE FROM profitAddStocks")
        print("表存在")
    else:
        # {code:股票代码,house:交易所, name:股票名称, price:当前价格,buy_price:买入价格, stop_surplus:止盈价格, stop_loss:止损价格,zdf:涨跌幅,hsl:换手率,syl:市盈率,sjl:市净率,zsz:总市值,ltsz:流通市值, type:类型}
        # 创建表
        cursor.execute("""CREATE TABLE IF NOT EXISTS profitAddStocks
                        (code TEXT PRIMARY KEY, house TEXT, name TEXT,price REAL,buy_price REAL,stop_surplus REAL,stop_loss REAL,zdf REAL,hsl REAL,syl REAL,sjl REAL,zsz REAL,ltsz REAL)""")



    # 遍历每一行数据

    for item in list:
        # 插入数据
        cursor.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?)", (0,0,0,0,0,0,'1'))


    # 提交事务
    conn.commit()

    # 查询数据
    cursor.execute("SELECT * FROM stocks")
    rows = cursor.fetchall()

    # 输出查询结果
    for row in rows:
        print(row)

    # 关闭游标和连接
    cursor.close()
    conn.close()

get_data(12)
