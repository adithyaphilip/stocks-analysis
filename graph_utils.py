import plotly.offline as pl
import plotly.graph_objs as go

import correlation
import data_util

import datetime

pl.init_notebook_mode()


def plot_line_graph(df1, df2, lag: datetime.timedelta = datetime.timedelta(days=0)):
    df1[data_util.KEY_DATE] = df1[data_util.KEY_DATE].apply(lambda date: date - lag)
    df1 = df1.sort_values(by=data_util.KEY_DATE)
    df2 = df2.sort_values(by=data_util.KEY_DATE)

    price1 = df1[data_util.KEY_OPEN_PRICE]
    price2 = df2[data_util.KEY_OPEN_PRICE]

    price1 = (price1 - price1.min()) / (price1.max() - price1.min())
    price2 = (price2 - price2.min()) / (price2.max() - price2.min())

    trace1 = go.Scatter(
        x=df1[data_util.KEY_DATE],
        y=price1,
        mode="lines+markers"
    )

    trace2 = go.Scatter(
        x=df2[data_util.KEY_DATE],
        y=price2,
        mode="lines+markers"
    )

    data = [trace1, trace2]

    pl.plot(data)
