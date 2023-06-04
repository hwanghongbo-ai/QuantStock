# coding=gbk
from pyecharts.charts import Kline
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
import numpy as np

FigurePath='figures/'
class YAxisInfo(object):
    def __init__(self):
        self.seriesname = ""
        self.yaxisdata = []
        self.itemstyleopts = opts.ItemStyleOpts()

class EchartRender(object):
    def __init__(self,width="1024px",height="720px",bgcolor=None):
        self.grid_chart = Grid(init_opts=opts.InitOpts(width=width, height=height,bg_color=bgcolor))

#List format
    def setXAxisData(self,data):
        self.xaxis = data


#values list
    #调用Line对象
    def drawLine(self, yaxisinfos,left,right,top,height,isshowxvalue=True,maintitle='',subtitle=''):
        line = self._makeline(self.xaxis,yaxisinfos,isshowxvalue=isshowxvalue,isshowyvalue=False,maintitle=maintitle,subtitle=subtitle)
        self.grid_chart.add(line,
                            grid_opts=opts.GridOpts(pos_left=left, pos_right=right, pos_top=top,height=height ),
                            )
        return line

    def drawBar(self,yaxisinfos,left,right,top,height,isshowxvalue,isshowyvalue,maintitle='',subtitle=''):
        bar = self._makeBar(self.xaxis, yaxisinfos,isshowxvalue=isshowxvalue,isshowyvalue=isshowyvalue,maintitle=maintitle,subtitle=subtitle)
        self.grid_chart.add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left=left, pos_right=right, pos_top=top, height=height
            )
        )

    #madf: dataframe,
    #ochldf: dataframe
    #画K线，调用Kline对象
    def drawKLine(self,left,right,top,height,ochldf,madf=None,seriesname='',maintitle='',subtitle=''):
        # 0， 初始变量
        overlap_kline_line = None
        # 1.画K线
        k_line = self._makeKline(np.round(ochldf.values, 2).tolist(),seriesname,maintitle=maintitle,subtitle=subtitle)  # must be


        # 2. 画 MA
        if not (madf is None):
            # sma = dict.get('sma')
            mas = madf.columns.tolist()
            for i in range(len(mas)):
                m = np.around(madf[str(mas[i])].values, 2).tolist()
                yaxisinfo = YAxisInfo()
                yaxisinfo.seriesname = str(mas[i])
                yaxisinfo.yaxisdata = m
                ma_line = self._makeline(self.xaxis,[yaxisinfo],isshowxvalue=False)
                if overlap_kline_line is None:
                    overlap_kline_line = k_line.overlap(ma_line)
                else:
                    overlap_kline_line.overlap(ma_line)

        if overlap_kline_line is None:
            self.grid_chart.add(
                k_line,
                grid_opts=opts.GridOpts(pos_left=left, pos_right=right, pos_top=top,height=height),
            )
        else:
            self.grid_chart.add(
                overlap_kline_line,
                grid_opts=opts.GridOpts(pos_left= left, pos_right= right, pos_top=top,height=height),
            )


    def drawVolumeBar(self,volumelists,bardata,left,right,top,height):
        # self.grid_chart.add_js_funcs("var barData = {}".format(ochl.values.tolist()))
        self.grid_chart.add_js_funcs("var barData = {}".format(bardata))
        itemstyle_opts=opts.ItemStyleOpts(
            color=JsCode(
                """
                 function(params) {
                    var colorList;
                    if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                        colorList = '#ef232a';
                    } else {
                        colorList = '#14b143';
                    }
                    return colorList;

                }
            """
            )
        )
        yaxisinfo = YAxisInfo()
        yaxisinfo.yaxisdata=volumelists
        yaxisinfo.itemstyleopts = itemstyle_opts
        vol_bar = self._makeBar(self.xaxis,[yaxisinfo],isshowxvalue=False,isshowyvalue=False)
        self.grid_chart.add(
            vol_bar,
            grid_opts=opts.GridOpts(
                pos_left= left, pos_right= right, pos_top=top, height=height
            )
        )

    def drawMacdBar(self,difs,deas,hists,left,right,top,height):
        # macd_bar = self._makeMacdBar(difs, deas, hists)
        macd_bar = self._makeMacd(difs, deas, hists)
        self.grid_chart.add(
            macd_bar,
            grid_opts=opts.GridOpts(
                pos_left= left, pos_right= right, pos_top=top, height=height
            )
        )


    def render(self,name ):
        self.grid_chart.render(name)

    def showChart(self,dict):
        ochl = dict.get('ochl')
        madf = None
        if 'sma' in dict:
            madf = dict.get('sma')
        self.drawKLine(ochl,madf,gridheight="50%")

        # Volumn 柱状图
        if 'vol' in dict:
            volumes = dict['vol']['volume']  # stock.getVolume(start,end)
            bardata = ochl.values.tolist()
            self.drawVolumeBar(volumes.values.tolist(),bardata=bardata,gridtop="55%",gridheight="15%")

        # MACD DIFS DEAS
        if 'macd' in dict:
            macd = dict.get('macd')  # stock.getMacd(start,end)
            difs=np.around(macd['DIF'].values, 2).tolist()
            deas= np.around(macd['DEA'].values, 2).tolist()
            hists=np.around(macd['HIST'].values, 2).tolist()
            self.drawMacdBar(difs,deas,hists,gridtop="75%",gridheight="25%")
        self.render("{}professional_kline_chart.html".format(FigurePath))

#调用Kline()
    def _makeKline(self,values,seriesname='',maintitle='',subtitle=''):
        kline = Kline()
        # kline.width = 1024
        # kline.height=720
        kline.add_xaxis(xaxis_data=self.xaxis)
        kline.add_yaxis(
            series_name=seriesname,
            y_axis=values,
            itemstyle_opts=opts.ItemStyleOpts(
                color="#ef232a",
                color0="#14b143",
                border_color="#ef232a",
                border_color0="#14b143",
            ),
            #标注收盘最高最低价
            # markpoint_opts=opts.MarkPointOpts(
            #     data=[
            #         opts.MarkPointItem(type_="max", name="最大值", value_index=2),
            #         opts.MarkPointItem(type_="min", name="最小值"),
            #     ]
            # ),
           #显示最高收盘或开盘价格
            # markline_opts=opts.MarkLineOpts(
            #     label_opts=opts.LabelOpts(
            #         position="middle", color="blue", font_size=15
            #     ),
            #     data=[opts.MarkLineItem(type_="max")],
            #     symbol=["circle", "none"],
            # ),
        )
        # kline.set_series_opts(
        #         # markarea_opts=opts.MarkAreaOpts(is_silent=True, data=split_data_part())
        #     markarea_opts=opts.MarkAreaOpts(is_silent=True)
        # )
        kline.set_global_opts(
            title_opts=opts.TitleOpts(title= maintitle, subtitle=subtitle),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,  # 缩放支持
                boundary_gap=True,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitline_opts=opts.SplitLineOpts(is_show=True), # 显示线
                # splitarea_opts=opts.SplitAreaOpts(  #显示灰白区间
                #     is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                # ),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            datazoom_opts=[
                opts.DataZoomOpts(type_="inside")
                # opts.DataZoomOpts(is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100),
            ],
            # 三个图的 axis 连在一块？？？
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, #显示线
                link=[{"xAxisIndex": "all"}],  #凡是用同样的xvalue的，都有一根连线关联
                label=opts.LabelOpts(background_color="#777"),
            )
        )
        return kline



    def _makeline(self, xaxis,yaxisinfos,isshowxvalue=True,isshowyvalue=False,maintitle='',subtitle=''):
        line = Line()
        line.add_xaxis(xaxis_data=xaxis)
        for yaxisinfo in yaxisinfos:
            line.add_yaxis(
                        series_name=yaxisinfo.seriesname,
                        y_axis=yaxisinfo.yaxisdata,
                        is_smooth=True,
                        linestyle_opts=opts.LineStyleOpts(opacity=0.5),
                        label_opts=opts.LabelOpts(is_show=isshowyvalue),
                    )
        line.set_global_opts(
                    title_opts={"text": maintitle, "subtext": subtitle},
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        # grid_index=1,
                        axislabel_opts=opts.LabelOpts(is_show=isshowxvalue),
                        is_scale=True,
                    ),
                    yaxis_opts=opts.AxisOpts(
                        is_scale=True,
                        # grid_index=1,
                        # split_number=3,
                        # axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                        # axistick_opts=opts.AxisTickOpts(is_show=False),
                        # splitline_opts=opts.SplitLineOpts(is_show=False),
                        # axislabel_opts=opts.LabelOpts(is_show=True),
                    ),
                    legend_opts=opts.LegendOpts(is_show=True), #控制seriesname是否出现，缺省True，这个语句可以不要,可以通过serieasname=‘’来不显示
                    datazoom_opts = [
                                        opts.DataZoomOpts(type_="inside")
                                        # opts.DataZoomOpts(is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100),
                                    ],
            )
        return line

    def _makeBar(self, xaxis,yaxisinfos,isshowxvalue=True,isshowyvalue=True,maintitle='',subtitle='',issupportdatazoom=False):
        bar= Bar()
        bar.add_xaxis(xaxis_data=xaxis)
        for yaxisinfo in yaxisinfos:
            bar.add_yaxis(
                    series_name=yaxisinfo.seriesname,
                    y_axis=yaxisinfo.yaxisdata,
                    itemstyle_opts=yaxisinfo.itemstyleopts,
                    # xaxis_index=1,
                    # yaxis_index=1,
                    label_opts=opts.LabelOpts(is_show=isshowyvalue)
                )
        if issupportdatazoom:
            datazoom_opts =[
                opts.DataZoomOpts(type_="inside")
                # opts.DataZoomOpts(is_show=True, type_="inside", xaxis_index=[0, 0], range_end=100)
                ]
        else:
            datazoom_opts = []
        bar.set_global_opts(
                title_opts={"text": maintitle, "subtext": subtitle},
                xaxis_opts=opts.AxisOpts(
                    # type_="category",
                    is_scale=True,
                    # grid_index=1,
                    axislabel_opts=opts.LabelOpts(is_show=isshowxvalue),
                ),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                ),
                legend_opts=opts.LegendOpts(is_show=True),  #控制seriesname是否出现，缺省True，这个语句可以不要
                datazoom_opts=datazoom_opts
                )
        return bar

    def _makeMacd(self,dif,dea,macdhist):
        itemstyle_opts = opts.ItemStyleOpts(
            color=JsCode(
                """
                    function(params) {
                        var colorList;
                        if (params.data >= 0) {
                          colorList = '#ef232a';
                        } else {
                          colorList = '#14b143';
                        }
                        return colorList;
                    }
                    """
            )
        )
        yaxisinfo = YAxisInfo()
        yaxisinfo.yaxisdata = macdhist
        yaxisinfo.itemstyleopts = itemstyle_opts

        hist_bar = self._makeBar(self.xaxis,[yaxisinfo],isshowxvalue=False,isshowyvalue=False)

        yaxisinfodif = YAxisInfo()
        yaxisinfodif.yaxisdata = dif
        # yaxisinfodif.seriesname="DIF"

        yaxisinfodea = YAxisInfo()
        yaxisinfodea.yaxisdata = dea
        # yaxisinfodea.seriesname="DEA"

        line = self._makeline(self.xaxis,[yaxisinfodif,yaxisinfodea],isshowxvalue=False,isshowyvalue=False)
        # line_2 = (
        #     Line()
        #         .add_xaxis(xaxis_data=self.xaxis)
        #         .add_yaxis(
        #             series_name="DIF",
        #             y_axis=dif,
        #             # xaxis_index=1,
        #             # yaxis_index=1,
        #             label_opts=opts.LabelOpts(is_show=False),
        #         )
        #         .add_yaxis(
        #             series_name="DEA",
        #             y_axis=dea,
        #             # xaxis_index=1,
        #             # yaxis_index=1,
        #             label_opts=opts.LabelOpts(is_show=False),
        #         )
        #         .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
        # )
        # 最下面的柱状图和折线图
        overlap_bar_line = hist_bar.overlap(line)
        return overlap_bar_line



    # def _makeMacdBar(self,dif,dea,macdhist):
    #     bar_2 = (
    #         Bar()
    #         .add_xaxis(xaxis_data=self.xaxis)
    #         .add_yaxis(
    #             series_name="MACD",
    #             y_axis=macdhist,
    #             xaxis_index=2,
    #             yaxis_index=2,
    #             label_opts=opts.LabelOpts(is_show=False),
    #             itemstyle_opts=opts.ItemStyleOpts(
    #                 color=JsCode(
    #                     """
    #                         function(params) {
    #                             var colorList;
    #                             if (params.data >= 0) {
    #                               colorList = '#ef232a';
    #                             } else {
    #                               colorList = '#14b143';
    #                             }
    #                             return colorList;
    #                         }
    #                         """
    #                 )
    #             ),
    #         )
    #         .set_global_opts(
    #             xaxis_opts=opts.AxisOpts(
    #                 type_="category",
    #                 grid_index=2,
    #                 axislabel_opts=opts.LabelOpts(is_show=False),
    #             ),
    #             yaxis_opts=opts.AxisOpts(
    #                 grid_index=2,
    #                 split_number=4,
    #                 axisline_opts=opts.AxisLineOpts(is_on_zero=False),
    #                 axistick_opts=opts.AxisTickOpts(is_show=False),
    #                 splitline_opts=opts.SplitLineOpts(is_show=False),
    #                 axislabel_opts=opts.LabelOpts(is_show=True),
    #             ),
    #             legend_opts=opts.LegendOpts(is_show=False),
    #         )
    #     )
    #
    #     line_2 = (
    #         Line()
    #         .add_xaxis(xaxis_data=self.xaxis)
    #         .add_yaxis(
    #             series_name="DIF",
    #             y_axis=dif,
    #             xaxis_index=2,
    #             yaxis_index=2,
    #             label_opts=opts.LabelOpts(is_show=False),
    #         )
    #         .add_yaxis(
    #             series_name="DEA",
    #             y_axis=dea,
    #             xaxis_index=2,
    #             yaxis_index=2,
    #             label_opts=opts.LabelOpts(is_show=False),
    #         )
    #         .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    #     )
    #     # 最下面的柱状图和折线图
    #     overlap_bar_line = bar_2.overlap(line_2)
    #     return overlap_bar_line

