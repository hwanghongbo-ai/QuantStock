# coding=utf-8
from datasource.WormsDataSource import WormsDataSource
from DBHelper import MySQLHelper
import pandas as pd
import win32api,win32con
from datetime import datetime
import time

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)

class TableFields(object):
    def __init__(self):
        self.BeiXiang=r"HOLD_DATE,CHANGE_RATE,ADD_MARKET_CAP,ADD_MARKET_RATE,HOLD_MARKET_CAP,HOLD_MARKET_RATE,\
        ADD_MARKET_BNAME, ADD_MARKET_NEWBCODE,BOARD_RATE_BNAME, BOARD_RATE_NEWBCODE,\
        MARKET_RATE_BNAME,MARKET_RATE_NEWBCODE,ADD_MARKET_MCODE,ADD_MARKET_MNAME, \
        ADD_SHARES_MCODE,ADD_SHARES_MNAME,MARKET_RATE_MCODE,MARKET_RATE_MNAME"
        self.Peavg = r"TRADE_DATE, CLOSE_PRICE, CHANGE_RATE, TOTAL_SHARES, FREE_SHARES, TOTAL_MARKET_CAP,FREE_MARKET_CAP,PE_TTM_AVG"
        self.oepnstop =r"trade_date, secu_code, secu_name, last_px, time, limit_up_days"
        self.downstop = r"trade_date, secu_code, secu_name, last_px, time"
        self.opendowninfo = r"trade_date, rise_num,fall_num, suspend_num,up_num,down_num,down_10,down_8,down_6,down_4,down_2,flat_num,up_2,up_4,up_6,up_8,up_10"


class DBFetcher(object):
    def saveBeiXiang2DB(self,type="",start=None,end=None):
        failedlist = []
        if not(self.confirm("是否要存储新数据到表beixiang{}：\n获取数据从{}到{}".format(type,start,end))):
            return False,failedlist
        wd = WormsDataSource()
        db = MySQLHelper()

        df = wd.wormBeiXiangEx(type,start=start,end=end)
        print(df)
        if df is None:
            print('No data Got')
            return False,failedlist
        if type=='hgt':
            table = 'beixianghgt'
        elif type == 'sgt':
            table = 'beixiangsgt'
        else:
            table = 'beixiang'
        sqlstrtemp = "insert into {}(HOLD_DATE,CHANGE_RATE,ADD_MARKET_CAP,ADD_MARKET_RATE,HOLD_MARKET_CAP,HOLD_MARKET_RATE,\
        ADD_MARKET_BNAME, ADD_MARKET_NEWBCODE,BOARD_RATE_BNAME, BOARD_RATE_NEWBCODE,\
        MARKET_RATE_BNAME,MARKET_RATE_NEWBCODE,ADD_MARKET_MCODE,ADD_MARKET_MNAME, \
        ADD_SHARES_MCODE,ADD_SHARES_MNAME,MARKET_RATE_MCODE,MARKET_RATE_MNAME) \
        values('{}',{},{}, {},{},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"

        # keys = df.columns.values
        for ix in range(df.shape[0]):
            record = df.iloc[ix]
            # sqlstr = sqlstrtemp.format(record['HOLD_DATE'], np.round(record['CHANGE_RATE'][:-1], record['zcsz'][:-1], record['zcszzb'][:-1],
            #                            record['zsz'][:-2], record['zszzb'][:-1], record['zdzcbk'], record['zbkbzj'],
            #                            record['zqscbzj'], record['zdzcszgg'], record['zdzcgsgg'], record['zgbzj'])
            sqlstr = sqlstrtemp.format(table,record['HOLD_DATE'], record['CHANGE_RATE'],  record['ADD_MARKET_CAP'] , record['ADD_MARKET_RATE'] ,
                                       record['HOLD_MARKET_CAP'] , record['HOLD_MARKET_RATE'] ,
                                       record['ADD_MARKET_BNAME'],record['ADD_MARKET_NEWBCODE'],record['BOARD_RATE_BNAME'],record['BOARD_RATE_NEWBCODE'],
                                       record['MARKET_RATE_BNAME'],record['MARKET_RATE_NEWBCODE'],record['ADD_MARKET_MCODE'],record['ADD_MARKET_MNAME'],
                                       record['ADD_SHARES_MCODE'],record['ADD_SHARES_MNAME'],record['MARKET_RATE_MCODE'],record['MARKET_RATE_MNAME'])
            print(sqlstr)
            if not(db.excute(sqlstr,True)):
                failedlist.append(record.values)
        return True,failedlist

    def savePEAVG2DB(self,symbol,datastart,start=None,end=None):
        failedlist = []
        if not(self.confirm("是否要存储新数据到表peavg{}：\n数据源起始{},\n获取数据从{}到{}".format(symbol,datastart,start,end))):
            return False,failedlist,None

        wd = WormsDataSource()
        db = MySQLHelper()
        df = wd.peavg(symbol=symbol, datastart=datastart,start=start, end=end)
        print(df)
        if df is None:
            print('No data Got')
            return False,failedlist,df
        table = "peavg{}".format(symbol)
        sqlstrtemp = "insert into {}(TRADE_DATE, CLOSE_PRICE, CHANGE_RATE, TOTAL_SHARES, FREE_SHARES, TOTAL_MARKET_CAP,FREE_MARKET_CAP,PE_TTM_AVG) \
           values('{}',{},{}, {},{},{},{},{})"

        # keys = df.columns.values
        for ix in range(df.shape[0]):
            record = df.iloc[ix]
            sqlstr = sqlstrtemp.format(table, record['TRADE_DATE'], record['CLOSE_PRICE'], record['CHANGE_RATE'],
                                       record['TOTAL_SHARES'], record['FREE_SHARES'], record['TOTAL_MARKET_CAP'],
                                       record['FREE_MARKET_CAP'], record['PE_TTM_AVG'] )
            print(sqlstr)
            if not (db.excute(sqlstr, True)):
                failedlist.append(record.values)
        return True,failedlist,df


    def confirm(self,message):
        res = win32api.MessageBox(0, message, "提醒", win32con.MB_OKCANCEL)
        if res == 1:
            return True
        return False

    def saveDailyUPDownStop2DB(self, type):
        if type=='zt':
            table = 'upstop'
            sqlstrtemp = "insert into {}(trade_date, secu_code, secu_name, last_px, time, limit_up_days) \
                         values('{}','{}','{}', {},'{}',{})"
        elif type=='dt':
            table = 'downstop'
            sqlstrtemp = "insert into {}(trade_date, secu_code, secu_name, last_px, time) \
                         values('{}','{}','{}', {},'{}')"
        elif type=='zb':
            table = 'upstopopen'
            sqlstrtemp = "insert into {}(trade_date, secu_code, secu_name, last_px, time) \
                         values('{}','{}','{}', {},'{}')"
        else:
            print('false')
            return False
        trade_date =datetime.now().strftime('%Y-%m-%d')
        # trade_date = "2023-06-02"
        if not (self.confirm("是否要存储{}数据到表{}".format(trade_date,table))):
            return False

        wd = WormsDataSource()
        db = MySQLHelper()

        df = wd.dailyupdownstop(type)
        print(df)
        if df is None:
            print('No data Got')
            return False

        result = True
        # keys = df.columns.values
        for ix in range(df.shape[0]):
            record = df.iloc[ix]
            if type=='zt':
                sqlstr = sqlstrtemp.format(table,trade_date, record['secu_code'], record['secu_name'], record['last_px'],record['time'], record['limit_up_days'])
            elif type == 'dt':
                sqlstr = sqlstrtemp.format(table, trade_date, record['secu_code'], record['secu_name'],record['last_px'], record['time'] )
            elif type == 'zb':
                sqlstr = sqlstrtemp.format(table, trade_date, record['secu_code'], record['secu_name'],record['last_px'], record['time'] )

            print(sqlstr)
            if not (db.excute(sqlstr, True)):
                result=False
        return result

    def saveDailyUPDownInfo2DB(self):
        table = 'updowninfo'
        sqlstrtemp = "insert into {} (trade_date, rise_num,fall_num, suspend_num,up_num,down_num,down_10,down_8,down_6,down_4,down_2,flat_num,up_2,up_4,up_6,up_8,up_10) \
                                         values('{}',{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})"
        trade_date = datetime.now().strftime('%Y-%m-%d')
        # trade_date = "2023-06-02"
        if not (self.confirm("是否要存储{}数据到表{}".format(trade_date, table))):
            return False

        wd = WormsDataSource()
        db = MySQLHelper()
        df = wd.dailyUpDownInfos()
        print(df)
        if df is None:
            print('No data Got')
            return False

        result = True
        # keys = df.columns.values
        for ix in range(df.shape[0]):
            record = df.iloc[ix]
            sqlstr = sqlstrtemp.format(table, trade_date, record['rise_num'], record['fall_num'],record['suspend_num'],
                                           record['up_num'], record['down_num'], record['down_10'],record['down_8'],
                                           record['down_6'], record['down_4'], record['down_2'], record['flat_num'],
                                           record['up_2'], record['up_4'], record['up_6'], record['up_8'], record['up_10'])


            print(sqlstr)
            if not (db.excute(sqlstr, True)):
                result = False
        return result


def task_dailyupdown(dbf):
    # UpDownTable
    actions1=['zt','dt','zb']
    for action in actions1:
        ret = dbf.saveDailyUPDownStop2DB(action)
        if ret:
            print('save up down stop action:{} is ok'.format(action))
        else:
            print('save up down stop action:{} is faild'.format(action))
        time.sleep(1)


    # updownInfo table
    ret = dbf.saveDailyUPDownInfo2DB()
    if ret:
        print('save updowninfo is ok')
    else:
        print('save updowninfo is failed')


def task_beixiang(dbf,start,end=None):
    actions = ['','hgt','sgt']
    for action in actions:
        ret,fl = dbf.saveBeiXiang2DB(type=action, start=start, end=end)
        if ret:
            print('save beixiang {} from {} to {} ok'.format(action,start,end))
        else:
            print('save beixiang failed')

def task_peavg(dbf,start,end=None):
    actions = ['000001', '000300', '399001','399006']
    for action in actions:
        ret,faillist,df = dbf.savePEAVG2DB(symbol=action,datastart=start,start=start)
        if ret:
            print('save peavg {} from {} to {} ok'.format(action, start, end))
            print(faillist)
        else:
            print('save peavg {} from {} to {} failed'.format(action, start, end))


if __name__ == '__main__':
    dbf = DBFetcher()
    task_dailyupdown(dbf)
    # task_beixiang(dbf,start='2022-09-08')
    # task_peavg(dbf,start='2022-04-20')






















    # 北向
    # ret,fl = dbf.saveBeiXiang2DB(type=None, start='2022-04-07', end=None)
    # if ret:
    #     print('save beixiang ok')
    # else:
    #     print('save beixiang failed')

    # pe
    # start1='2010-01-01'
    # start2= '2019-01-19'
    # start3='2021-02-09'
    # ret,faillist,df = dbf.savePEAVG2DB(symbol='000300',datastart=start3)
    # if ret:
    #     print('save ok')
    #     print(faillist)
    #     print(df['TRADE_DATE'].values[0],df['TRADE_DATE'].values[-1])
    #     print(df.iloc[[0,-1]])
    # else:
    #     print('save failed')

    # UpDownTable
    # ret = dbf.saveDailyUPDownStop2DB('zb')
    # if ret:
    #     print('save updown is ok')
    # else:
    #     print('save updown is failed')

    # updownInfo table
    # ret = dbf.saveDailyUPDownInfo2DB()
    # if ret:
    #     print('save updowninfo is ok')
    # else:
    #     print('save updowninfo is failed')
