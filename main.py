import numpy as np

from getStockBasic import getStockBasic
from createTable import createTable_stockBasic,createTable_daily
from getStockDaily import getStockDaily
from chooseTrategy.trendReverse import wMA10MinPlessMA5MinP
from dailyToGraph import dailyGraph
from straResearch import MAminPointDate,MAmaxPointDate,volPeak,selectStockData,getStockList,drawMa
from choTrategy import MA55MinPMA20MinPMA4MinP
import pandas as pd
import tushare as ts
import pymysql
def main():
    #ts.set_token('895b931bf65d2f2cece35a9999ec9531eed552bebc376ec091bf4298')#如果token失效执行一次
    #createTable_stockBasic() #建表：A股列表，执行一次即可
    #getStockBasic()#获取A股列表，执行一次即可，后续若需要更新可再定期执行
    #createTable_daily() #建表：A股日交易行情后复权数据，执行一次即可
    #print(pro)
    #getStockDaily()#日常更新数据执行此语句即可
    """刚刚建立数据库需执行以下大批量下载数据的语句"""
    """
    downloading=1
    while downloading:
        if downloading == 0:
            break
        getStockDaily()
    """
    #dailyGraph('602833.sz')#画k线
    #stoc=getStockList()
    #selectStockData('002415.sz', '20191231', '20220727')
    #df= selectStockData('002415.sz', '20141231', '20170601')
    #print(df)
    #vpeakInd=volPeak(df)
    #drawMa(df)
    #print(MAminPointDate(df['MA20']))
    #print(volPeak(df))
    #MA55MinPMA20MinPMA4MinP()
    wMA10MinPlessMA5MinP()


if __name__ == '__main__':

    print('begin:gogogogogogo')
    main()


    print('completed!!!')


