from datasource.QuantDataSourceManager import QuantDataSourceManager

class QuantTools(object):

    '''
    获取最近的交易日
    '''
    @staticmethod
    def GetLatestTradeDate(exchange='SZSE'):
        juejingdatasource = QuantDataSourceManager().jueJingDataSource()
        return juejingdatasource.getLatestTradeDate(exchange)


    """
      获取当日A股代码（剔除次新股，退市股和非上市股）
       :exchanges: 多个交易所代码可用 ,(英文逗号)分割, 也支持 ['exchange1', 'exchange2'] , 默认 None 表示所有
       :param new_days:新股上市天数，默认为365天
    """
    @staticmethod
    def getStocks(exchanges=None, skip_list_days=0):
        juejingdatasource = QuantDataSourceManager().jueJingDataSource()
        return juejingdatasource.get_normal_stocks(exchanges=exchanges,skip_list_days=skip_list_days)

    '''
     获取symbols列表中的股票的当日涨跌幅
    '''
    @staticmethod
    def getUpperLowLimitPrice(symbols):
        juejingdatasource = QuantDataSourceManager().jueJingDataSource()
        return juejingdatasource.getUpperLowlimitPrice(symbols)
