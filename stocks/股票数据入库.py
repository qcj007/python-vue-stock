import pandas as pd
import os
import sqlite3
def read_excel_file(filename, sheet_name="选股结果"):
    """
    读取Excel文件的指定sheet，并返回数据帧。
    :param filename: Excel文件的路径
    :param sheet_name: 要读取的sheet名称，默认为'选股结果'
    :return: 数据帧
    """
    try:
        # 使用绝对路径读取文件
        file_path = os.path.join(os.getcwd(), filename)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        print(f"读取Excel文件时发生错误：{e}")
        return None

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


def writeInDb():
    # 读取excel的某个sheet
    df = read_excel_file("assets/data.xlsx", sheet_name="选股结果")

    # 连接数据库或创建新数据库
    conn = sqlite3.connect("assets/stockDataBase.db")
    # 创建游标
    cursor = conn.cursor()
    # {code:股票代码,house:交易所, name:股票名称, price:当前价格,buy_price:买入价格, stop_surplus:止盈价格, stop_loss:止损价格,zdf:涨跌幅,hsl:换手率,syl:市盈率,sjl:市净率,zsz:总市值,ltsz:流通市值}

    if table_exists(conn, "supportLevelStocks"):
        # 清空supportLevelStocks表
        cursor.execute("DELETE FROM supportLevelStocks")
    else:
        # 创建表
        cursor.execute("""CREATE TABLE IF NOT EXISTS supportLevelStocks
                        (code TEXT PRIMARY KEY, house TEXT, name TEXT,price REAL,buy_price REAL,stop_surplus REAL,stop_loss REAL,zdf REAL,hsl REAL,syl REAL,sjl REAL,zsz REAL,ltsz REAL)""")

    # 遍历每一行数据
    if df is not None:
        for index, row in df.iterrows():
            stockCode = row["股票代码"]
            list= stockCode.split(".")
            code = list[0]
            house = list[1]
            name = row["股票简称"]
            price = row["当前股价"]
            buy_price = row["买入"]
            stop_surplus = row["止盈"]
            stop_loss = row["止损"]
            
            if buy_price>0:
                # 插入数据
                cursor.execute("INSERT INTO supportLevelStocks VALUES (?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?)", (code,house,name,price,buy_price,stop_surplus,stop_loss,0,0,0,0,0,0))


    # 提交事务
    conn.commit()

    # 查询数据
    cursor.execute("SELECT * FROM supportLevelStocks")
    rows = cursor.fetchall()

    # 输出查询结果
    for row in rows:
        print(row)

    # 关闭游标和连接
    cursor.close()
    conn.close()

writeInDb()