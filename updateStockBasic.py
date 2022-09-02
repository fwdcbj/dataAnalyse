#更新“股票列表”数据
import getStockBasic as td
import pandas as pd
def truncate_update(engine, data, table_name):
    """删除mysql表所有数据，to_sql追加新数据"""
    data=pd.DataFrame(data)
    conn = engine.connect()
    conn.execute('truncate ' + table_name)
    data.to_sql(table_name, engine, if_exists='append', index=False)

def update_stock_basic(engine, pro, retry_count, pause):
    """更新 股票信息 所有数据"""
    data = td.get_stock_basic(pro, retry_count, pause)
    truncate_update(engine, data, 'stock_basic')