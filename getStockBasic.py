import tushare as ts
from sqlalchemy.types import DATE, CHAR, VARCHAR
from sqlalchemy import create_engine
"""获取A股上市公司列表，存入本地数据库"""

def getStockBasic():

    pro = ts.pro_api()
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print(df.head(5))
# df1.to_excel('D:/workplace/db/basics1.xlsx')
    engine = create_engine("mysql+mysqldb://pythonuser:password@127.0.0.1/mysql?charset=utf8")
    DTYPES = {'ts_code': VARCHAR(10), 'symbol': VARCHAR(10), 'name': VARCHAR(20), 'area': VARCHAR(20),\
              'industry': VARCHAR(20),'market':VARCHAR(20),'list_date': DATE}
    df.to_sql('stockBasic', con=engine, dtype=DTYPES, if_exists='append', index=True, index_label='id')