from matplotlib.axis import XAxis
import pandas_datareader as web
import datetime as dt
import streamlit as st
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from pandas_datareader._utils import RemoteDataError

start=dt.datetime(2018,1,1).strftime("%Y-%m-%d")
end=dt.datetime.today().strftime("%Y-%m-%d")


st.title("Stock Prediction using FBProphet")

selected_stocks=st.text_input("Which stock to forecast?")
selected_stocks=selected_stocks.upper()
def load_data(ticker):
    try:
        print("Data from Yahoo Finance")
        data= web.DataReader(ticker,"yahoo",start,end)
    except RemoteDataError:
        print("Yahoo Finance Down, using TIINGO")
        data = web.get_data_tiingo(ticker, start,end, api_key=('1d1fc93985b7038a58402f0f1e906ac08626a293'))

    data.columns = [x.lower() for x in data.columns]
    data.reset_index(inplace=True)
    data['date']=data['date'].dt.tz_localize(None)
    return data


#n_years=st.slider("years of prediction",1,4)
#period=n_years*365

#data=load_data(selected_stocks)
#st.subheader("Raw Data")
#st.write(data.tail())


def plot_raw_data():
    #layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig = go.Figure(data=[go.Candlestick(x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])#,layout=layout)
    #fig.layout.update(title_text=f"Times Series Data of {selected_stocks} from {start} to {end} ",xaxis_rangeslider_visible=True)
    fig.update_layout(title_text=f"Times Series Data of {selected_stocks} from {start} to {end} ")
    fig.update_layout(autosize=False, width=800, height=500, margin=dict(l=50,r=50,b=100,t=100,pad=4),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    return fig
    #st.plotly_chart(fig)

find_button=st.button("Find Stock")

n_years=3
period=n_years*365
#plot_raw_data()
def forecast():
    df_train=data[["date","close"]]
    df_train =df_train.rename(columns={"date":"ds","close":"y"})
    m=Prophet()
    m.fit(df_train)
    future=m.make_future_dataframe(periods=period)
    forecast=m.predict(future)
    fig=plot_plotly(m,forecast, trend=True, changepoints=True)
    fig.update_layout(autosize=False, width=800, height=500, margin=dict(l=50,r=50,b=100,t=100,pad=4),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(title_text="Forecast of upcoming 3 years")
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    return fig
    #st.plotly_chart(fig_fore)


if find_button==True:
    data=load_data(selected_stocks)
    st.plotly_chart(plot_raw_data())
    st.plotly_chart(forecast())
