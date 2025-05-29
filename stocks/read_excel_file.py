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