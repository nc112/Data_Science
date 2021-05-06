import requests
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from json import load as jsload
import matplotlib.pyplot as plt

# Define the params
const_URL = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'


'''
reference of how to trigger fetch action
URL of the data：
http://fund.eastmoney.com/f10/F10DataApi.aspx

example of fetching data(provide necessary params)：
http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=110022&page=1&sdate=2019-01-01&edate=2019-02-13&per=20

> description of params
    "type": "lsjz", 历史净值
    "code": 110011, 基金代码
    "page": 1, per指定了每页的显示条数，存在一页显示不完整的情况，该参数直接指定显示第几页；
    "per":  指定每页显示的条数，如果不指定该参数，则默认值为10，如果指定该参数值在1-49之间，
            则每页条数按照指定参数值显示，如果指定该值大于等于50，则每页显示20条
    "sdate": "2021-03-30" 数据开始日期 
    "edate": "2021-04-30" 数据结束日期
'''


def fetch_params(html_data):
    assert html_data is not None
    params = {
        'all_pages_number': 0,
        'all_heads': []
    }
    soup = BeautifulSoup(html_data, 'html.parser')
    pattern = re.compile(r'pages:(.*),')
    result = re.search(pattern, html_data).group(1)
    pages = int(result)
    params['all_pages_number'] = pages

    assert soup is not None
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])
    params['all_heads'] = heads.copy()
    return params


def get_url_data(url, params=None):
    assert url is not None
    resp = requests.get(url, params)
    resp.raise_for_status()
    return resp.text


def fetch_fund_data(fund_params, code=''):
    assert code != ''
    fund_params['code'] = code
    print(fund_params)

    resp_data = get_url_data(const_URL, fund_params)
    data_inputs = fetch_params(resp_data)

    # Fetch all page contents
    records = []
    for page in range(1, data_inputs['all_pages_number']+1):
        # update page number here
        fund_params['page'] = page
        html = get_url_data(const_URL, fund_params)
        soup = BeautifulSoup(html, 'html.parser')

        # fetch all fund data
        for row in soup.findAll("tbody")[0].findAll("tr"):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents

                # remove the value which is not a number
                if val == []:
                    row_records.append(np.nan)
                else:
                    row_records.append(val[0])

            # record data
            records.append(row_records)

    # trim data and record to dataframe
    np_records = np.array(records)
    data = pd.DataFrame()
    for col, col_name in enumerate(data_inputs['all_heads']):
        data[col_name] = np_records[:, col]
    return data


def draw_figure(data):
    # Fix chinese and '-' display issue
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # trim data
    data['净值日期'] = pd.to_datetime(data['净值日期'], format='%Y/%m/%d')
    data['单位净值'] = data['单位净值'].astype(float)
    data['累计净值'] = data['累计净值'].astype(float)
    data['日增长率'] = data['日增长率'].str.strip('%').astype(float)
    data = data.sort_values(by='净值日期',
                            axis=0,
                            ascending=True).reset_index(drop=True)

    # coordinate Axis update
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data['净值日期'], data['单位净值'])
    ax1.plot(data['净值日期'], data['累计净值'])
    ax1.set_ylabel('净值数据')
    ax1.set_xlabel('日期')
    plt.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(data['净值日期'],  data['日增长率'], 'r')
    ax2.set_ylabel('日增长率（%）')
    plt.legend(loc='upper right')
    plt.title('基金净值数据')
    plt.show()

    bonus = data['累计净值'] - data['单位净值']
    plt.figure()
    plt.plot(data['净值日期'], bonus)
    plt.xlabel('日期')
    plt.ylabel('累计净值-单位净值')
    plt.title('基金“分红”信息')
    plt.show()


# Data analyze
def data_analyze_from_police(data):
    assert data is not None
    data['日增长率'] = data['日增长率'].str.strip('%').astype(float)
    print('日增长率缺失总天数：', sum(np.isnan(data['日增长率'])))
    print('日增长率>0的天数：', sum(data['日增长率'] > 0))


# 易方达中小盘混合: 110011
if __name__ == "__main__":
    with open('./config/config.json') as config_file:
        config_params = jsload(fp=config_file)
    data = fetch_fund_data(fund_params=config_params['fund_get_params'],
                           code=config_params['fund_code_list']['zhongou_shidaixianfeng'])

    print('data:', data)
    # update figure
    draw_figure(data)
    data_analyze_from_police(data)

    # for debug, highlight the data
    #print(data)
