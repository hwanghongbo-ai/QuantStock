# coding=utf-8
from datasource.HbDataSource import HbDataSource
from render.EchartRender import EchartRender
from render.EchartRender import YAxisInfo
from render.EchartRender import FigurePath
from database.DBHelper import MySQLHelper
import pandas as pd
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#显示所有行
pd.set_option('display.max_rows', None)
pd.set_option('display.width',1000)

#python画图
class QuantCharter(object):

#平均市盈率，指数走势
    def indexVsAvgPE(self,index,start=None,end=None):
        hbds = HbDataSource()
        data =  hbds.getAvgPEdata(index,start=start,end=end)
        echart = EchartRender()
        xv = data["TRADE_DATE"].dt.strftime('%Y-%m-%d').values.tolist()
        echart.setXAxisData(xv)
        yaixsinfo = YAxisInfo()
        yaixsinfo.yaxisdata = data['CLOSE_PRICE'].values.tolist()

        yaixsinfo1 = YAxisInfo()
        yaixsinfo1.yaxisdata = (data['CLOSE_PRICE']/data['PE_TTM_AVG']).values.tolist()

        yaixsinfo2 = YAxisInfo()
        yaixsinfo2.yaxisdata = (data['PE_TTM_AVG']).values.tolist()

        echart.drawLine([yaixsinfo1],left=80,right=50,top=10,height=200,isshowxvalue=True,maintitle="指数",subtitle=index)
        echart.drawLine([yaixsinfo], left=80, right=50, top=260, height=200, isshowxvalue=True, maintitle="指数",
                        subtitle=index)
        echart.drawLine([yaixsinfo2], left=80, right=50, top=500, height=200, isshowxvalue=True, maintitle="指数",
                        subtitle=index)


        echart.render("{}indexVsAvgPE.html".format(FigurePath))


    def updownstopbar(self,days):
        mysql = MySQLHelper()
        sql = r"select trade_date, up_num,down_num from updowninfo where trade_date in ("
        for day in days:
            sql = sql+ "\'"+day+"\',"
        sql = sql[:-1]+")"
        data = mysql.selectbypd(sql)
        print(data)
        zbsql = r"select trade_date,count(*) num from upstopopen  where trade_date in ("
        for day in days:
            zbsql = zbsql+ "\'"+day+"\',"
        zbsql = zbsql[:-1]+") group by trade_date"
        zbdata = mysql.selectbypd(zbsql)
        print(zbdata)

        echart = EchartRender()
        xv = data["trade_date"].dt.strftime('%Y-%m-%d').values.tolist()

        echart.setXAxisData(xv)
        yupaixsinfo = YAxisInfo()
        yupaixsinfo.yaxisdata = data['up_num'].values.tolist()
        yupaixsinfo.seriesname="up stop number"
        ydownaixsinfo = YAxisInfo()
        ydownaixsinfo.yaxisdata = data['down_num'].values.tolist()
        ydownaixsinfo.seriesname = "down stop number"
        yupopenaixsinfo = YAxisInfo()
        yupopenaixsinfo.yaxisdata = zbdata['num'].values.tolist()
        yupopenaixsinfo.seriesname = "up open number"

        echart.drawBar([yupaixsinfo,ydownaixsinfo,yupopenaixsinfo],left=80,right=50,top=100,height=200,isshowxvalue=True,isshowyvalue=True,maintitle="Up Dwon stop Number")
        echart.render("{}updownstopbar.html".format(FigurePath))

        print("render chart ok")


if __name__ == '__main__':

    # %%
    qct = QuantCharter()
    qct.indexVsAvgPE('000300')

    # %%
    qct = QuantCharter()
    qct.updownstopbar(['2022-04-15','2022-04-18','2022-04-19','2022-04-20'])
    # qct.updownstopbar([  '2022-04-18', '2022-04-19', '2022-04-20'])