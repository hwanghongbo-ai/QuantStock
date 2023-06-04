
from DBHelper import MySQLHelper


def createBeiXiangTable(db):
    table = "BeiXiang"
    keys = ['Id','HOLD_DATE', 'CHANGE_RATE', 'ADD_MARKET_CAP', 'ADD_MARKET_RATE', 'HOLD_MARKET_CAP', 'HOLD_MARKET_RATE',
            'ADD_MARKET_BNAME', 'ADD_MARKET_NEWBCODE','BOARD_RATE_BNAME','BOARD_RATE_NEWBCODE','MARKET_RATE_BNAME', 'MARKET_RATE_NEWBCODE',
            'ADD_MARKET_MCODE', 'ADD_MARKET_MNAME', 'ADD_SHARES_MCODE', 'ADD_SHARES_MNAME', 'MARKET_RATE_MCODE', 'MARKET_RATE_MNAME']

    types=["int","datetime","float","float","float","float","float",
           "varchar(20)","varchar(10)","varchar(20)","varchar(10)","varchar(20)","varchar(10)",
           "varchar(10)","varchar(20)","varchar(10)","varchar(20)","varchar(10)","varchar(20)"]
    indexes = [True,False,False,False,False,False,False,
               False,False,False,False,False,False,
               False,False,False,False,False,False]
    nulls = ['NOT NULL','','','','','','',
             '','','','','','',
             '','','','','','']
    defaluts=["auto_increment",'','','','','','',
             '','','','','','',
             '','','','','','']

    print('id is {}'.format(id(db)))
    if db.createTable(table=table,keys=keys,types=types,nulls=nulls,defualts=defaluts,indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))



def createPEAVGTable(symbol,db):
    table = "peavg{}".format(symbol)
    keys = ['Id','TRADE_DATE', 'CLOSE_PRICE', 'CHANGE_RATE', 'TOTAL_SHARES', 'FREE_SHARES', 'TOTAL_MARKET_CAP',
                'FREE_MARKET_CAP', 'PE_TTM_AVG']

    types=["int","datetime","float","float","float","float","float","float","float"]
    indexes = [True,False,False,False,False,False,False,False,False]
    nulls = ['NOT NULL','','','','','','', '','']
    defaluts=["auto_increment",'','','','','','','','']
    if db.createTable(table=table,keys=keys,types=types,nulls=nulls,defualts=defaluts,indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))


def createUpStopTable(db):
    table = 'UpStop'
    keys = ["Id", "trade_date", "secu_code", "secu_name", "last_px", "time", "limit_up_days"]
    types = ["int", "datetime", "varchar(20)", "varchar(20)", "float", "datetime", "int"]
    indexes = [True, False, False, False, False, False, False]
    nulls = ['NOT NULL', '', '', '', '', '', '']
    defaluts = ["auto_increment", '', '', '', '', '', '']

    if db.createTable(table=table, keys=keys, types=types, nulls=nulls, defualts=defaluts, indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))


def createDownStopTable(db):
    table = 'DownStop'
    keys = ["Id", "trade_date", "secu_code", "secu_name", "last_px", "time"]
    types = ["int", "datetime", "varchar(20)", "varchar(20)", "float", "datetime"]
    indexes = [True, False, False, False, False, False]
    nulls = ['NOT NULL', '', '', '', '', '' ]
    defaluts = ["auto_increment", '', '', '', '', '' ]

    if db.createTable(table=table, keys=keys, types=types, nulls=nulls, defualts=defaluts, indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))

#炸板
def createUpStopOpenTable(db):
    table = 'upstopopen'
    keys = ["Id", "trade_date", "secu_code", "secu_name", "last_px", "time"]
    types = ["int", "datetime", "varchar(20)", "varchar(20)", "float", "datetime"]
    indexes = [True, False, False, False, False, False]
    nulls = ['NOT NULL', '', '', '', '', '' ]
    defaluts = ["auto_increment", '', '', '', '', '' ]

    if db.createTable(table=table, keys=keys, types=types, nulls=nulls, defualts=defaluts, indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))


#炸板
def createUpDownInfosTable(db):
    table = 'UpDownInfo'
    keys = ["Id", "trade_date", "rise_num","fall_num",
            "suspend_num","up_num","down_num","down_10",
            "down_8","down_6","down_4","down_2",
            "flat_num","up_2","up_4","up_6",
            "up_8","up_10"]
    types = ["int", "datetime", "int", "int",
             "int", "int", "int", "int",
             "int", "int", "int", "int",
             "int", "int", "int", "int",
             "int", "int"]
    indexes = [True, False, False, False,
               False, False, False, False,
               False, False, False, False,
               False, False, False, False,
               False, False]
    nulls = ['NOT NULL', '', '', '',
             '', '' , '', '',
             '', '' , '', '',
             '', '' , '', '',
             '', '' ]
    defaluts = ["auto_increment", '', '', '',
                '', '','', '' ,
                '', '','', '' ,
                '', '','', '' ,
                '', '']

    if db.createTable(table=table, keys=keys, types=types, nulls=nulls, defualts=defaluts, indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))


def createTable(db,table):
    keys = ['Id','HOLD_DATE', 'CHANGE_RATE', 'ADD_MARKET_CAP', 'ADD_MARKET_RATE', 'HOLD_MARKET_CAP', 'HOLD_MARKET_RATE',
            'ADD_MARKET_BNAME', 'ADD_MARKET_NEWBCODE','BOARD_RATE_BNAME','BOARD_RATE_NEWBCODE','MARKET_RATE_BNAME', 'MARKET_RATE_NEWBCODE',
            'ADD_MARKET_MCODE', 'ADD_MARKET_MNAME', 'ADD_SHARES_MCODE', 'ADD_SHARES_MNAME', 'MARKET_RATE_MCODE', 'MARKET_RATE_MNAME']

    types=["int","datetime","float","float","float","float","float",
           "varchar(20)","varchar(10)","varchar(20)","varchar(10)","varchar(20)","varchar(10)",
           "varchar(10)","varchar(20)","varchar(10)","varchar(20)","varchar(10)","varchar(20)"]
    indexes = [True,False,False,False,False,False,False,
               False,False,False,False,False,False,
               False,False,False,False,False,False]
    nulls = ['NOT NULL','','','','','','',
             '','','','','','',
             '','','','','','']
    defaluts=["auto_increment",'','','','','','',
             '','','','','','',
             '','','','','','']

    # print('id is {}'.format(id(db)))
    if db.createTable(table=table,keys=keys,types=types,nulls=nulls,defualts=defaluts,indexes=indexes):
        print("success to create table {}".format(table))
    else:
        print("fail to create table {}".format(table))

if __name__ == '__main__':
    db = MySQLHelper()
    # createBeiXiangTable(db)
    # createPEAVGTable('000300',db)
    # createUpStopTable(db)
    # createDownStopTable(db)
    # createUpStopOpenTable(db)
    # createUpDownInfosTable(db)




    createTable(db,'abc')
    # createTable(db,'dddd')