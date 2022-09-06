'''趋势反转：周线反转，底部放量'''

import numpy as np
from getStockBasic import getStockBasic
from createTable import createTable_stockBasic,createTable_daily
from getStockDaily import getStockDaily
from dailyToGraph import dailyGraph
from straResearch import MAminPointDate,MAmaxPointDate,volPeak,selectStockData,getStockList,drawMa
import pandas as pd
import tushare as ts
import pymysql
import datetime
def wMA10MinPlessMA5MinP():
    #dailyGraph('602833.sz')#画k线
    #stocks=getStockList()
    stos = pd.read_excel("stoclist.xlsx",usecols=[2])

    for stoc in stos.values:
        stoc=''.join(stoc)#转换数据格式
        eDate='20220830'
        df= selectStockData(stoc, '20210801', eDate)
        #print(df)
        periodType='W' #采样周期，可以是W（周）、M（月）、Q季度
        weekDf=df.resample(periodType).last()
        df.to_excel('temp\/'+ stoc +'day.xlsx')
        weekDf.to_excel('temp\/'+ stoc +'week.xlsx')





        ma55min = MAminPointDate(df['MA55']).tolist()
        ma20min = MAminPointDate(df['MA20']).tolist()
        ma20max = MAmaxPointDate(df['MA20'])
        ma4min = MAminPointDate(df['MA4'])
        ma4max = MAmaxPointDate(df['MA4'])

        df['MA4-MA20'] = df['MA4']-df['MA20']
        #df['comMA4P&MA20'] = df['comMA4P&MA20'].apply(lambda x: 10000 if x.index.isin(ma20max))
        #df['comMA4P&MA20'] = df.loc[ma4min].apply(lambda x: -1 if x <= df.loc[ma4min,'MA20'] )
        print(df.tail(20))
        print(df.loc[ma4max])
        df['comMA4P&MA20']=0
        #df.loc[[ma20minl]]['MA20'].values



        if ( len(ma55min) <=0 or len(ma20min) <=2) :#( len(ma55min) <=0 or len(ma20min) <=2)
            continue
        ma20minl = ma20min.pop()
        ma20minl2 = ma20min.pop()

        #print(float(df.loc[[ma20minl]]['MA20'].values-df.loc[[ma20minl2]]['MA20'].values)/float(df.loc[[ma20minl2]]['MA20'].values))
        ma55minl = ma55min.pop()
        dMA20min=float(df.loc[[ma20minl]]['MA20'].values - df.loc[[ma20minl2]]['MA20'].values)
        percDMA20min=dMA20min/float(df.loc[[ma20minl2]]['MA20'].values)
        if percDMA20min>=0.01:
            continue
        if ((datetime.datetime.strptime(eDate,'%Y%m%d') - ma20minl).days <=5 and ma20minl >= ma55minl):
            print('okkkkkkkkkkkkkkkkk')
            print('倒数第1个寄点')
            print(df.loc[[ma20minl]])
            print('倒数第二个寄点')
            print(df.loc[[ma20minl2]])
            #print('ma55min:')
            #print(ma55minl)
            print('ma20min:')
            print(ma20minl)
            print(stoc)
            drawMa(df)
            #sleep(8)


    #vpeakInd=volPeak(df)
    #drawMa(df)
    #print(MAminPointDate(df['MA20']))
    #print(volPeak(df))
    return 0