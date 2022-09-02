import pymysql
def createTable_stockBasic():
    # 建立连接通道，建立连接填入（连接数据库的IP地址，端口号，用户名，密码，要操作的数据库，字符编码）

    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql", charset="utf8")
    # 创建游标，操作设置为字典类型，返回结果为字典格式！不写默认是元组格式！
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 操作数据库的sql语句
    sql1 = "drop table if exists stockBasic"
    r = cursor.execute(sql1)
    res = cursor.fetchone()  # 接收返回的第一行数据
    print(res)
    #ret = cursor.fetchmany(n)  # 接收返回的n行数据
    #req = cursor.fetchall()  # 接收返回的说有数据
    # 写完发送操作语句之后，就需要把更改的数据提交，不然数据库无法完成新建或是修改操作
    conn.commit()  # 提交
    sql2= "create table stockBasic(id int comment '序号',\
    ts_code  varchar(10) comment 'TS股票代码', \
    symbol  varchar(10)   comment '股票代码', \
    name    varchar(20)   comment '股票名称',\
    area    varchar(20)  comment '所在地域',\
    industry    varchar(20)  comment '所属行业',\
    market   varchar(20)  comment '市场类型 （主板/中小板/创业板）',\
    list_date  char(8)  comment '上市日期',\
    primary key(symbol) comment'股票代码作为主键'\
            ) COMMENT '全部股票清单'"

    r = cursor.execute(sql2)
    res = cursor.fetchone()  # 接收返回的第一行数据
    print(res)
    conn.commit()  # 提交
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接
def createTable_daily():
    conn = pymysql.connect(user="pythonuser", password="password", host="localhost", database="mysql", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = "drop table if exists daily"
    r = cursor.execute(sql1)
    res = cursor.fetchone()  # 接收返回的第一行数据
    print(res)
    conn.commit()  # 提交
    sql2 = "create table daily(id int NOT NULL comment '序号',\
    ts_code  varchar(10) comment 'TS股票代码',\
    trade_date char(8)  comment '交易日期',\
    openP float comment '开盘价',\
    high float comment '最高价',\
    low float comment '最低价',\
    closeP float comment '收盘价',\
    pre_close float comment '昨收价',\
    chg float comment '涨跌额',\
    pct_chg float comment '涨跌幅',\
    vol float comment '成交量(手)',\
    amount float comment '成交额(千元)',\
    primary key(ts_code,trade_date) comment '股票代码交易日期日期作为联合主键'\
            )comment '后复权日交易行情'"
    r = cursor.execute(sql2)
    res = cursor.fetchone()  # 接收返回的第一行数据
    print(res)
    conn.commit()  # 提交
    cursor.close()  # 关闭游标
    conn.close()  # 关闭连接



