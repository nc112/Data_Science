import pandas as pd
import matplotlib.pyplot as plt


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
