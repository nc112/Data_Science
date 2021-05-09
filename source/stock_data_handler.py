import tushare as ts
import datetime

China_stockindex_list = [
    "399006", # sz399006 创业板指
    "000001", # sh000001 上证指数
    "399001", # sz399001 深证成指
    "000300", # sh000300 沪深300
    "399005", # sz399005 中小板指
]
start_time = '20200401'
time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
end_time = time_temp.strftime('%Y%m%d')

def init_tushare():
    ts.set_token('8f80c6835195ef288e59a1c17cec01739f61e876ce92651b21acc1d2')
    return  ts.pro_api()

def test_func(pro):
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20200401'
    time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
    end_dt = time_temp.strftime('%Y%m%d')
    # 建立数据库连接,剔除已入库的部分
    #db = pymysql.connect(host='127.0.0.1', user='root', passwd='admin', db='stock', charset='utf8')
    #cursor = db.cursor()
    # 设定需要获取数据的股票池
    stock_pool = ['399006.SZ']
    total = len(stock_pool)
    # 循环获取单个股票的日线行情
    for i in range(len(stock_pool)):
        try:
            df = pro.index_daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
			# 打印进度
            print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
            print("data frame:", df)
            c_len = df.shape[0]
        except Exception as aa:
            print(aa)
            print('No DATA Code: ' + str(i))
            continue
        # for j in range(c_len):
        #     resu0 = list(df.ix[c_len-1-j])
        #     resu = []
        #     for k in range(len(resu0)):
        #         if str(resu0[k]) == 'nan':
        #             resu.append(-1)
        #         else:
        #             resu.append(resu0[k])
        #     state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
            #print
        
            #try:
                #sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8]))
                #cursor.execute(sql_insert)
                #db.commit()
            #except Exception as err:
              #  continue
    #cursor.close()
    #db.close()
    #print('All Finished!')

def get_daily(self, ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df 


def print_data(code, s_date=None, e_date=None):
    pro.trade_cal(exchange='SSE', is_open='1', 
                    start_date='20200101', 
                    end_date='20200401', 
                    fields='cal_date')



if __name__ == "__main__":
    ts_pro = init_tushare()
    test_func(ts_pro)
    #print_data(China_stockindex_list[0], s_date='2021-04-01', e_date='2021-5-9')