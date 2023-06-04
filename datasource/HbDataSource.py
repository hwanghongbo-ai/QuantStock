# coding=utf-8
from database.DBHelper import MySQLHelper

class HbDataSource(object):

#type:hgt, sgt, None
    '''
       返回北向数据
       type：
       hgt: 沪股通
       sgt: 深股通
       None: 北向
    '''
    def getBeixiangData(self,type=None,fields=None,start = None,end=None):
        mysql = MySQLHelper()
        if type == 'hgt':
            table = 'beixianghgt'
        elif type == 'sgt':
            table = 'beixiangsgt'
        else:
            table = 'beixiang'
        if fields is None:
            fields = r"HOLD_DATE,CHANGE_RATE,ADD_MARKET_CAP,ADD_MARKET_RATE," \
                 r"HOLD_MARKET_CAP,HOLD_MARKET_RATE,ADD_MARKET_BNAME, " \
                 r"ADD_MARKET_NEWBCODE,BOARD_RATE_BNAME, BOARD_RATE_NEWBCODE," \
                 r"MARKET_RATE_BNAME,MARKET_RATE_NEWBCODE,ADD_MARKET_MCODE," \
                 r"ADD_MARKET_MNAME, ADD_SHARES_MCODE,ADD_SHARES_MNAME," \
                 r"MARKET_RATE_MCODE,MARKET_RATE_MNAME"
        if not (start is None) and (end is None):
            sql = "select {} from {} where HOLD_DATE >='{}'".format(fields,table, start)
        elif (start is None) and not (end is None):
            sql = "select {} from {} where HOLD_DATE <='{}'".format(fields,table, end)
        elif not (start is None) and not (end is None):
            sql = "select {} from {} where HOLD_DATE between '{}' and '{}'".format(fields,table, start, end)
        else:
            sql = "select {} from {}".format(fields,table)
        print(sql)
        return mysql.selectbypd(sql)


    # 获取指定日期的涨停板（upstop），跌停板（downstop），涨停开板（upstopopen） 返回df数据
    def getUpdownStopdata(self,type,start,end):
        if type=='upstop':
            table = 'upstop'
        elif type == 'downstop':
            table = 'downstop'
        elif type == 'upstopopen':
            table = 'upstopopen'
        else:
            return None
        if (start is None) and (end is None):
            sql = r"select * from {}".format(table)
        elif (start is None) and not(end is None):
            sql = r"select * from {} where trade_date<='{}'".format(table,end)
        elif not(start is None) and   (end is None):
            sql = r"select * from {} where trade_date>='{}'".format(table, start)
        elif start != end:
            sql = r"select * from {} where trade_date between '{}' and '{}'".format(table, start,end)
        else:
            sql = r"select * from {} where trade_date ='{}'".format(table, start)
        mysql = MySQLHelper()
        return mysql.selectbypd(sqlstr=sql)


   # 获取指定日期的涨停板（upstop），跌停板（downstop），涨停开板（upstopopen） 总数。
    def getUpDownStopCount(self,type,start=None,end=None):
        if type == 'upstop':
            table = 'upstop'
        elif type == 'downstop':
            table = 'downstop'
        elif type == 'upstopopen':
            table = 'upstopopen'
        else:
            return -1
        if (start is None) and (end is None):
            sql = r"select count(*) from {}".format(table)
        elif (start is None) and not (end is None):
            sql = r"select count(*) from {} where trade_date<='{}'".format(table, end)
        elif not (start is None) and (end is None):
            sql = r"select count(*) from {} where trade_date>='{}'".format(table, start)
        elif start != end:
            sql = r"select count(*) from {} where trade_date between '{}' and '{}'".format(table, start, end)
        else:
            sql = r"select count(*) from {} where trade_date ='{}'".format(table, start)
        mysql = MySQLHelper()
        res = mysql.select(sql)
        # print(res)
        if len(res) > 0:
            if len(res[0])>0:
                return res[0][0]
        return 0

 # 获取指定日期的涨跌信息数据
    def getRiseFallDetails(self,field="*",start=None,end=None):
        table = 'updowninfo'
        if (start is None) and (end is None):
            sql = r"select {} from {}".format(field,table)
        elif (start is None) and not(end is None):
            sql = r"select {} from {} where trade_date<='{}'".format(field,table,end)
        elif not(start is None) and (end is None):
            sql = r"select {} from {} where trade_date>='{}'".format(field,table, start)
        elif start != end:
            sql = r"select {} from {} where trade_date between '{}' and '{}'".format(field,table, start,end)
        else:
            sql = r"select {} from {} where trade_date ='{}'".format(field,table, start)
        mysql = MySQLHelper()
        return mysql.selectbypd(sqlstr=sql)

# 获取指定周期内指数的平均PE
    def getAvgPEdata(self,type,start=None,end=None):
        if type=='000001':
            table = 'peavg000001'
        elif type == '000300':
            table = 'peavg000300'
        elif type == '399001':
            table = 'peavg399001'
        elif type=='399006':
            table = 'peavg399006'
        else:
            return None
        if (start is None) and (end is None):
            sql = r"select * from {}".format(table)
        elif (start is None) and not(end is None):
            sql = r"select * from {} where trade_date<='{}'".format(table,end)
        elif not(start is None) and   (end is None):
            sql = r"select * from {} where trade_date>='{}'".format(table, start)
        elif start != end:
            sql = r"select * from {} where trade_date between '{}' and '{}'".format(table, start,end)
        else:
            sql = r"select * from {} where trade_date ='{}'".format(table, start)
        mysql = MySQLHelper()
        return mysql.selectbypd(sqlstr=sql)

#获取历史上连板days的股票
    def getContinuousUpStopSymbols(self,date,days):
        sql = "select * from upstop where trade_date='{}' and limit_up_days >= {} ".format(date,days)
        mysql = MySQLHelper()
        db = mysql.selectbypd(sqlstr=sql)
        return db

    def getHighestUpStopDays(self,start=None,end=None):
        if (start is None) and (end is None):
            sql = r"select trade_date,max(limit_up_days) from upstop group by trade_date "
        elif (start is None) and not (end is None):
            sql = r"select trade_date,max(limit_up_days) from upstop where trade_date <='{}' group by trade_date".format(end)
        elif not (start is None) and (end is None):
            sql = r"select trade_date,max(limit_up_days) from upstop where trade_date >='{}' group by trade_date".format(start)
        elif start != end:
            sql = r"select trade_date,max(limit_up_days) from upstop where trade_date between '{}' and '{}' group by trade_date ".format(start, end)
        else:
            sql = r"select trade_date,max(limit_up_days) from upstop where trade_date ='{}'".format(start)
        mysql = MySQLHelper()
        db = mysql.selectbypd(sqlstr=sql)
        return db































































 # def getBeixiangData(self,type=None,fields=None,start=None,end=None):
    #     mysql = MySQLHelper()
    #     if type=='hgt':
    #         table = 'beixianghgt'
    #     elif type == 'sgt':
    #         table = 'beixiangsgt'
    #     else:
    #         table = 'beixiang'
    #
    #
    #     if fields is None:
    #         fields = r"HOLD_DATE,CHANGE_RATE,ADD_MARKET_CAP,ADD_MARKET_RATE,HOLD_MARKET_CAP,HOLD_MARKET_RATE,\
    #         ADD_MARKET_BNAME, ADD_MARKET_NEWBCODE,BOARD_RATE_BNAME, BOARD_RATE_NEWBCODE,\
    #         MARKET_RATE_BNAME,MARKET_RATE_NEWBCODE,ADD_MARKET_MCODE,ADD_MARKET_MNAME, \
    #         ADD_SHARES_MCODE,ADD_SHARES_MNAME,MARKET_RATE_MCODE,MARKET_RATE_MNAME"
    #     if not(start is None) and (end is None):
    #         sql = "select {} from {} where HOLD_DATE >='{}'".format(fields,table,start)
    #     elif (start is None) and not(end is None):
    #         sql = "select {} from {} where HOLD_DATE <='{}'".format(fields,table, end)
    #     elif not(start is None) and not(end is None):
    #         sql = "select {} from {} where HOLD_DATE between '{}' and '{}'".format(fields,table, start,end)
    #     else:
    #         sql = "select {} from {}".format(fields,table)
    #     print(sql)
    #     records = mysql.select(sql)
    #     return records