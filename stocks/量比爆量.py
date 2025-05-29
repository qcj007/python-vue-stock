import requests
import json
import pandas as pd
import os
import sqlite3


# 当日涨跌幅，近5天量比和成交量，当天量比大于2， 涨跌幅-1%~4%，企业市值小于50亿，市值从小到大排列
# 筛选出：
# 1.当日换手率大于4   
# 2.量比： ①当天量比大于3，前一天量比大于2      ②当天量比大于2，前面四天量比小于1.2
# 交易当天交易方法：
# 1.开盘买：买入价格设置日线支撑位，可以高一两分
# 2.尾盘买：看放量是否比前一天高或者齐平


def get_data(number):
    headers = {
        "Content-Type":"application/json",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer":"https://www.iwencai.com/unifiedwap/result?w=%E8%BF%913%E5%A4%A9%E9%87%8F%E6%AF%94&querytype=stock&addSign=1741853779346",
        "Cookie":"other_uid=Ths_iwencai_Xuangu_442513wdw38ls6xxxh1op2v16mv8bohz; ta_random_userid=z83ludqtey; cid=0f147d4af3ef617b77f6cdccbb9073411741851328; v=Ax8xVnfYhAT-BYAYNc-gGZ2XrnishHIqjdh3GrFsu04VQDEmuVQDdp2oB3vC"
    }



    source = "Ths_iwencai_Xuangu"
    version = "2.0"
    query_area = ""
    block_list = ""
    add_info = "{\"urp\":{\"scene\":1,\"company\":1,\"business\":1},\"contentType\":\"json\",\"searchInfo\":true}"
    question = "当日涨跌幅，近5天每天量比，当天量比大于2， 涨跌幅-1%~4%，企业市值小于50亿，市值从小到大排列"
    perpage = 100
    page = 1
    secondary_intent = "stock"
    log_info = "{\"input_type\":\"typewrite\"}"
    rsh = "Ths_iwencai_Xuangu_442513wdw38ls6xxxh1op2v16mv8bohz"

    data = f"""{{
        "source": "{source}",
        "version": "{version}",
        "query_area": "{query_area}",
        "block_list": "{block_list}",
        "add_info": "{add_info}",
        "question": "{question}",
        "perpage": "{perpage}",
        "page": {page},
        "secondary_intent": "{secondary_intent}",
        "log_info": "{log_info}",
        "rsh": "{rsh}"
    }}"""




    # data = f"query=%E5%B9%B4%E6%8A%A5%E9%A2%84%E5%A2%9E&urp_sort_way=desc&urp_sort_index=%E9%A2%84%E5%91%8A%E5%87%80%E5%88%A9%E6%B6%A6%E5%8F%98%E5%8A%A8%E5%B9%85%E5%BA%A6%5B20231231%5D&page={number}&perpage=100&addheaderindexes=&condition=%5B%7B%22dateText%22%3A%22%E5%B9%B4%E6%8A%A5%22%2C%22indexName%22%3A%22%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%2C%22indexProperties%22%3A%5B%22%E8%B5%B7%E5%A7%8B%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231231%22%2C%22%E6%88%AA%E6%AD%A2%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%2020231231%22%2C%22%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%3E-%3C%E6%89%AD%E4%BA%8F%3E-%3C%E9%A2%84%E5%A2%9E%22%5D%2C%22dateUnit%22%3A%22%E5%B9%B4%22%2C%22source%22%3A%22new_parser%22%2C%22type%22%3A%22index%22%2C%22indexPropertiesMap%22%3A%7B%22%E8%B5%B7%E5%A7%8B%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231231%22%2C%22%E6%88%AA%E6%AD%A2%E4%BA%A4%E6%98%93%E6%97%A5%E6%9C%9F%22%3A%2220231231%22%2C%22%E5%8C%85%E5%90%AB%22%3A%22%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%3E-%3C%E6%89%AD%E4%BA%8F%3E-%3C%E9%A2%84%E5%A2%9E%22%7D%2C%22reportType%22%3A%22FUTURE_QUARTER%22%2C%22dateType%22%3A%22%E6%8A%A5%E5%91%8A%E6%9C%9F%22%2C%22chunkedResult%22%3A%22%E5%B9%B4%E6%8A%A5%E9%A2%84%E5%A2%9E%22%2C%22valueType%22%3A%22_%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%2C%22domain%22%3A%22abs_%E8%82%A1%E7%A5%A8%E9%A2%86%E5%9F%9F%22%2C%22uiText%22%3A%22%E5%B9%B4%E6%8A%A5%E7%9A%84%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%7C%E6%89%AD%E4%BA%8F%7C%E9%A2%84%E5%A2%9E%22%2C%22sonSize%22%3A0%2C%22queryText%22%3A%22%E5%B9%B4%E6%8A%A5%E7%9A%84%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%E5%8C%85%E5%90%AB%E5%A4%A7%E5%B9%85%E4%B8%8A%E5%8D%87%7C%E6%89%AD%E4%BA%8F%7C%E9%A2%84%E5%A2%9E%22%2C%22relatedSize%22%3A0%2C%22tag%22%3A%22%5B%E5%B9%B4%E6%8A%A5%5D%E4%B8%9A%E7%BB%A9%E9%A2%84%E5%91%8A%E7%B1%BB%E5%9E%8B%22%7D%5D&codelist=&indexnamelimit=&logid=33355461f6d81c4c095271354f8b7a10&ret=json_all&sessionid=33355461f6d81c4c095271354f8b7a10&source=Ths_iwencai_Xuangu&date_range%5B0%5D=20231231&date_range%5B1%5D=20231231&iwc_token=0ac9664917106828099447570&urp_use_sort=1&user_id=270967397&uuids%5B0%5D=24087&query_type=stock&comp_id=6836372&business_cat=soniu&uuid=24087"
    url = "https://www.iwencai.com/customized/chart/get-robot-data"
    res = requests.post(url, headers=headers, data=data)
    # # res.encoding = "utf-8"
    print(res.status_code)

    # json_data = res.json()  # 解析JSON数据
    # print(json_data)
    # result = json_data.get("answer")


    # stockFile = open('movies.json', 'w', encoding='utf-8')
    # stockFile.write(f'{json.dumps(result)}')
    # return result



get_data(12)
