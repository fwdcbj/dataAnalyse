import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pymysql
import mplfinance as mpf
from datetime import datetime as dt, timedelta
import numpy as np
import scipy.signal as signal

'''本地数据库gu列表'''
def getStockList():
    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql",charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select ts_code from stockBasic"

    cursor.execute(sql)
    res = cursor.fetchall()  # 接收返回的所有数据
    df = pd.DataFrame(res)
    #df.to_excel('stoclist.xlsx')
    #for i in df['ts_code']:
        #print(i)
    #print(type(df))
    return df


'''本地数据库抽取数据,返回df'''
def selectStockData(code,SDate,EDate):
    #print(code)
    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql",charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from daily where ts_code=%s and trade_date> %s  and trade_date< %s order by trade_date"
    codeSDateEDate=[code,SDate,EDate]
    #cursor.execute(sql, ['002415.sz', '20160231', '20220727'])
    cursor.execute(sql,codeSDateEDate)
    res = cursor.fetchall()  # 接收返回的所有数据

    df = pd.DataFrame(res, columns=['ts_code','trade_date', 'openP', 'high', 'low', 'closeP', 'vol'])
    #print(df)
    df.columns = ['ts_code','trade_date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df.set_index("trade_date", inplace=True)
    df['MA4'] = df['Close'].rolling(window=4).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA55'] = df['Close'].rolling(window=55).mean()
    df['MA4-MA20'] = df['MA4'] - df['MA20']
    df['MA20-MA55'] = df['MA20'] - df['MA55']
    df['Close-MA20'] = df['Close'] - df['MA20']
    #print(df)
    return df

'''求极大值日期，df为均线列数据'''
def MAmaxPointDate(df):
    if df.ndim ==1:
        x = df.values        
        maxP=signal.argrelextrema(x, np.greater)[0]
        return (df.index[maxP])
    else:
        print("输入参数格式有误")
        return 0

'''求极小值日期,df为均线列数据'''
def MAminPointDate(df):
    if df.ndim ==1:
        x = df.values
        minP=signal.argrelextrema(-x, np.greater)[0]
        #print("极小值日期是")
        #print(df.index[minP])
        return (df.index[minP])
    else:
        print("输入参数格式有误")
        return 0

'''交易量peak'''
def volPeak(df):
    df['pre_3vol'] = df['Volume'].rolling(window=5).mean().shift(1)
    volP=df['Volume'][(df['Volume'] / df['pre_3vol']) > 1.3]
    print("交易量突点volP")
    return volP

'''均线、成交量'''
def drawMa(df):
    #print(df)
    fig,ax=plt.subplots(nrows=3,ncols=1,sharex='all',sharey=False,figsize=(16, 9))
    fig.subplots_adjust(hspace=0,wspace=0)

    ax1=ax[0]
    ax1.plot(df.index,df['MA55'],label='MA55')
    ax1.plot(df.index,df['MA20'],label='MA20')
    ax1.plot(df.index,df['MA4'],label='MA4')
    ax1.set_title( df.iloc [1,0])

    ax1.legend()

    ax2=ax[1]
    ax2.plot(df.index,df['Volume'],label='VOL')
    ax2.legend()
    #plt.show()
    #plt.pause(2)
    plt.savefig('pic\/'+ df.iloc[1,0] + '.jpg')

    plt.close()
    #return volP
























def MApeak():
    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql",
                           charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from daily where ts_code=%s and trade_date> %s  and trade_date< %s order by trade_date"
    cursor.execute(sql, ['002415.sz', '20140231', '20180727'])
    res = cursor.fetchall()  # 接收返回的所有数据
    df = pd.DataFrame(res, columns=['trade_date', 'openP', 'high', 'low', 'closeP', 'vol'])
    df.columns = ['trade_date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df.set_index("trade_date", inplace=True)
    df['MA8'] = df['Close'].rolling(window=4).mean()
    df['MA80'] = df['Close'].rolling(window=20).mean()
    '''求极值点参考'''
    '''
    x = df['MA8'].values
    plt.plot(np.arange(len(x)), x)
    plt.plot(signal.argrelextrema(x, np.greater)[0], x[signal.argrelextrema(x, np.greater)], 'o')#极大值
    plt.plot(signal.argrelextrema(-x, np.greater)[0], x[signal.argrelextrema(-x, np.greater)], '+')#极小值
    '''
    x = df['MA8'].values
    print(type(df['MA8']))
    print(df['MA8'].ndim)
    print(x.shape)
    maxP=signal.argrelextrema(x, np.greater)[0]
    plt.plot(df['MA8'].index, df['MA8'].values)
    plt.plot(df['MA8'].index[maxP],df['MA8'][maxP], '1')
    print(df['MA8'].index[maxP])


    minP=signal.argrelextrema(-x, np.greater)[0]
    plt.plot(df['MA8'].index, df['MA8'].values)
    plt.plot(df['MA8'].index[minP],df['MA8'][minP], '+')
    plt.plot(df['MA80'].index, df['MA80'].values)
    plt.show()
