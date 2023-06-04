
TimeColumnName= "time"
CodeColumnName = "symbol"
Echart_OCHL=['open','close','low','high']

class Freq:
    Min_1 = 1
    Min_5 = 2
    Min_10 = 3
    Min_15 = 4
    Min_30 = 5
    Min_60 = 6
    Day = 7
    Week = 8
    Month = 9
    Year = 10



class Exchange(object):
    Jue_SHANGHAI = 'SHSE'
    Jue_SHENGZHENG = 'SZSE'
    Bao_SHANGHAI = 'sh'
    Bao_SHENGZHENG = 'sz'

    @staticmethod
    def Symbol(exchange,code):
        return ".".join([exchange,code])

class TradeDataField(object):
    Close = 'close'
    Open = 'open'
    High = 'high'
    Low = 'low'
    Volumn = 'volume'
    Amount = 'amount'



class UpDownInfoField(object):
    Rise = 'rise_num'
    Fall = 'fall_num'
    UpStop = 'up_num'
    DownStop = 'down_num'
    UP8p10 = 'up10'
    UP6p8  = 'up8'
    UP4p6 = 'up6'
    UP2p4 = 'up4'
    UP0p2 = 'up2'
    Flat = 'flat_num'
    Down0p2 = 'down_2'
    Down2p4 = 'down_4'
    Down4p6 = 'down_6'
    Down6p8 = 'down_8'
    Down8p10 = 'down_10'