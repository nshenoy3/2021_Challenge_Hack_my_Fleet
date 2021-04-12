import pandas as pd
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
from math import pi
import statistics
from bokeh.models.widgets import Div
from bokeh.layouts import column


def getFuelInsights (dataset):
    print("Loading fuel insights")
    groupedDict = dataset.groupby(['Asset type', 'AssetID']).apply(lambda x: dict(zip(x['Date'], x['Fuel Level (%)']))).to_dict()
    fuelData = {}
    for key in groupedDict.keys():
        value = groupedDict[key]
        tmp = 0
        lastDate = '0'
        refilDates = {}
        for date in value.keys():
            if tmp == 0:
                tmp = value[date]
                lastDate = date
                continue
            if (int(value[date]) > int(tmp)):
                d0 = datetime.datetime(int(lastDate.split("-")[0]), int(lastDate.split("-")[1]), int(lastDate.split("-")[2]))
                d1 = datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]))
                delta = d1 - d0
                refilDates[pd.to_datetime(date, format='%Y-%m-%d')] = delta.days
                lastDate = date
            tmp = value[date]
        fuelData[str(key[0])+"_"+str(key[1])] = refilDates
    print("Loaded Fuel Insights")
    return fuelData


def showFuelInsightsFor(fuelData, asssetId = "1022017", assetType = "Excavator"):
    p = figure(title="Fuel Refill Dates vs days it worked before refill", x_axis_label='Refill Date',
               y_axis_label='No of Days', plot_width=1000)
    x = list(fuelData[assetType + "_" + asssetId].keys())
    y = list(fuelData[assetType + "_" + asssetId].values())
    p.circle(x, y, fill_alpha=0.2, size=5)
    p.xaxis.formatter = DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = pi/4
    # lastDate = x[-1]
    # # A naive approach to choose the next prediction date.
    # # We can use Machine learning time series prediction (ARIMA Approach) to predict the next few dates for refill.
    # delta = statistics.mode(y)
    # nextPredictedDate = lastDate + datetime.timedelta(days=delta)
    # print("Next Refill Date : " + nextPredictedDate)
    output_file("./templates/Fuel.html")

    div_exp00 = Div(
        text=""" <b>FUEL REFILL HISTORY GRAPH</b>
                    """,
        width=300, style={'font-size': '100%'})
    div_exp01 = Div(
        text=""" This graph analyses the history of fuel refills that happened for each asset ID. Predicting the next refill date can help us figure out when a particular asset needs fuel and can help us set alerts.""",
        width=300)
    show(column(div_exp00, div_exp01, p))


