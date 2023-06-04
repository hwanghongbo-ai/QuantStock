# coding=utf-8
import baostock as bs
from config.StockConfig import Freq
from config.StockConfig import TimeColumnName
from config.StockConfig import CodeColumnName

class BaoDataSource(object):

    def __init__(self):
        self.islg = self.connect()


    def __freq(self,klinetype):
        _type = "m"
        if klinetype == Freq.Min_1:
            freq = '1'
        elif klinetype == Freq.Min_5:
            freq = '5'
        elif klinetype == Freq.Min_15:
            freq = '15'
        elif klinetype == Freq.Min_30:
            freq = '30'
        elif klinetype == Freq.Min_60:
            freq = '60'
        elif klinetype == Freq.Day:
            freq = 'd'
            _type = "d"
        elif klinetype == Freq.Week:
            freq = 'w'
            _type = "d"
        elif klinetype == Freq.Month:
            freq = 'm'
            _type = "d"
        elif klinetype == Freq.Year:
            freq = 'y'
            _type = "d"
        else:
            freq = klinetype
            if freq=='d' or freq=='w' or freq=='m' or freq=='y':
                _type = "d"
        return freq,_type



    def connect(self):
        self.lg = bs.login()
        if self.lg.error_code != '0':
            self.islg = False
        else:
            self.islg = True
        return self.islg


    def disconnect(self):
        print("----disconnect---------")
        if self.islg:
            bs.logout(self.lg.user_id)

    # 指数不支持分时数据
    def getData(self, code, freq, start_date,end_date,istimeindex=False):
        if not self.islg:
            return None
        freq,_type = self.__freq(freq)
        columns =  "code,open,close,low,high,volume,amount,date"
        if _type=="m":
            columns = "code,open,close,low,high,volume,amount,time"

        rs = bs.query_history_k_data_plus(code,
                                          # "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          columns,
                                          start_date= start_date, end_date= end_date,
                                          frequency=freq, adjustflag="3")

        if rs.error_code != '0':
            print('query_history_k_data_plus respond error_code:' + rs.error_code)
            print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
            return None
        df = rs.get_data()
        if df.empty:
            return df
        df.rename(columns={'date': TimeColumnName,'code':CodeColumnName}, inplace=True)
        if istimeindex is True:
             df.set_index(TimeColumnName,inplace=True)
        # df.index = df['date']
        df['open']= df['open'].astype('float64')
        df['close'] = df['close'].astype('float64')
        df['high'] = df['high'].astype('float64')
        df['low'] = df['low'].astype('float64')
        df['volume'] = df['volume'].astype('float64')
        df['amount'] = df['amount'].astype('float64')

        return df





