from sqlalchemy.types import DATE, CHAR, VARCHAR, Float
from sqlalchemy import create_engine
import pandas as pd
import pymysql
from datetime import datetime as dt, timedelta
import time
import mplfinance as mpf

def dailyGraph(code):

    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql",
                           charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    ts_code=code

    daily_code = "select * from daily where ts_code='%s' and trade_date>'20160520'  and trade_date<'20210630' order by trade_date" %ts_code

    r = cursor.execute(daily_code)
    res2 = cursor.fetchall()  # 接收返回的所有数据
    #print("res2:",res2)
    #print(type(res2))
    df=pd.DataFrame(res2,columns=['trade_date','openP','high', 'low', 'closeP','vol'])
    df.columns=['trade_date','Open','High','Low','Close','Volume']
    #print(df.head())

    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df.set_index("trade_date", inplace=True)
    df1=df.copy()
    #df1["Changepercent"]= df1["Close"].diff()
    df1['Changepercent'] = (df1["Close"].pct_change()).apply(lambda x: format(x, '0.001'))
    df1['Changepercent']=df1['Changepercent'].astype(float)
    df1["MA5"]=df1["Close"].rolling(window=5).mean()

    print(df1)

    print((df1[df1['Changepercent']>0.02]).index)

    MA10=df1["Close"].rolling(window=10).mean()

    print("MA10:")
    print(MA10)
   # print(df1)
    #mpf.plot(df,type='candle')
    #mpf.plot(df,type='candle',mav=(3,5,10),volume=True,show_nontrading=False)
    mpf.plot(df, type="candle",style='blueskies', ylabel='Kxian',volume=True, tight_layout=True,datetime_format='%Y%m%d',mav=(3,5,10))

