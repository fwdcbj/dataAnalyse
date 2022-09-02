import tushare as ts
import pymysql
from sqlalchemy.types import DATE, CHAR, VARCHAR, Float
from sqlalchemy import create_engine

from datetime import datetime as dt, timedelta
import time

def getStockDaily():

    engine = create_engine("mysql+mysqldb://pythonuser:password@127.0.0.1/mysql?charset=utf8")
    DTYPES = {'ts_code': VARCHAR(10), 'trade_date': DATE, 'openP': Float, 'high': Float, 'low': Float, 'closeP': Float, \
              'pre_close': Float, 'chg': Float, 'pct_chg': Float, 'vol': Float, 'amount': Float}

    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    stockBasic_code = "select ts_code,list_date from stockBasic"
    r = cursor.execute(stockBasic_code)
    res1 = cursor.fetchall()  # 接收返回的所有数据
    #print(res1)
    daily_code = "select ts_code,max(trade_date) as trade_date from daily group by ts_code"

    r = cursor.execute(daily_code)
    res2 = cursor.fetchall()  # 接收返回的所有数据
    #print("res2:",res2)


    if res2:
        for ts_code in res2:
            global downloading
            #print(ts_code['ts_code'], ts_code['trade_date'])
            #print("ts_code['trade_date']",ts_code['trade_date'])
            startdate =str((dt.strptime(ts_code['trade_date'], "%Y%m%d")+timedelta(days=1)).date()).replace('-', '')
            #print("startdate:",startdate)
            enddate = dt.strptime(ts_code['trade_date'], "%Y%m%d")
            if enddate >=dt.now()+ timedelta(days=-10): #判断距当前时间间隔少于10天的话，只获取当前时间前十天的数据进行入库
                """大批量下载数据时启用,将days=-10改成days=-100，启用以下continue语句"""
                """
                print("ts_code:",ts_code['ts_code'])
                print("skip......")
                print("startdate:", startdate)
                continue
                """
                print("Last round")
                print("startdate:",startdate)
                print('dt.now() + timedelta(days=-10):',dt.now()+ timedelta(days=-10))
                #print("endtdate:", enddate)
                enddate = str((dt.strptime(ts_code['trade_date'], "%Y%m%d")+timedelta(days=12)).date()).replace('-', '')
                print("endtdate:", enddate)
                time.sleep(0.15)
                df = ts.pro_bar(ts_code=ts_code['ts_code'], adj='hfq', start_date=startdate,end_date=enddate)
                if df is not None:

                    df.columns = ['ts_code', 'trade_date', 'openP', 'high', 'low', 'closeP', 'pre_close', 'chg',
                                  'pct_chg', 'vol', 'amount']
                    df.to_sql('daily', con=engine, dtype=DTYPES, if_exists='append', index=True, index_label='id')
                    print(".............code:",)
                    print('...........newstartdate:', startdate)
                    print(".............endtdate:", enddate)
                    print(".............gucode:", ts_code['ts_code'])
                    #downloading=0
                    time.sleep(0.15)

                else:
                    downloading=0
                    print("********gucode:", ts_code['ts_code'])
                    time.sleep(0.15)
                    continue






            else:

                #print("lastenddate:",enddate.date())
                startdate=str(enddate.date()+timedelta(days=1)).replace('-', '')
                enddate = str(enddate.date()+timedelta(days=30)).replace('-', '')
                #print('...........newstartdate:',startdate)
                #print(".............endtdate:", enddate)
                #print(".............gucode:",ts_code['ts_code'])
                df = ts.pro_bar(ts_code=ts_code['ts_code'], adj='hfq', start_date=startdate, end_date=enddate)
                #print(df)
                if df is None:
                    print("ts_code['ts_code'] skip:",ts_code['ts_code'])
                    print(dt.now())
                    continue

                df.columns = ['ts_code', 'trade_date', 'openP', 'high', 'low', 'closeP', 'pre_close', 'chg', 'pct_chg','vol', 'amount']
                df.to_sql('daily', con=engine, dtype=DTYPES, if_exists='append', index=True, index_label='id')
                time.sleep(0.3)

    else:
        for ts_code in res1:
            print("first insert to daily")
            enddate = dt.strptime(ts_code['list_date'],"%Y%m%d")
            enddate=str((enddate+timedelta(days=3031)).date()).replace('-','')
            df = ts.pro_bar(ts_code=ts_code['ts_code'], adj='hfq', start_date= ts_code['list_date'], end_date=enddate)
            #print(df)
            df.columns = ['ts_code', 'trade_date', 'openP', 'high', 'low', 'closeP', 'pre_close', 'chg', 'pct_chg', \
                          'vol', 'amount']
            #print(df)
            df.to_sql('daily', con=engine, dtype=DTYPES, if_exists='append', index=True, index_label='id')
            time.sleep(0.3)



    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接

