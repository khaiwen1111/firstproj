from unicodedata import name
import pandas_datareader as web
import datetime as dt
import streamlit as st
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from pandas_datareader._utils import RemoteDataError

start=dt.datetime(2018,1,1)
end=dt.datetime.today().strftime("%Y-%m-%d")


st.title("Stock Prediction App")
stocks=("AAPL","GOOG")
selected_stocks =st.selectbox("Select dataset for precition",stocks)
n_years=st.slider("years of prediction",1,4)
period=n_years*365

def load_data(ticker):
    try:
        data= web.DataReader(ticker,"yahoo",start,end)
    except RemoteDataError:
        print("Yahoo Finance Down, using TIINGO")
        data = web.get_data_tiingo(ticker, start,end, api_key=('1d1fc93985b7038a58402f0f1e906ac08626a293'))

    data.columns = [x.lower() for x in data.columns]
    data.reset_index(inplace=True)
    data['date']=data['date'].dt.tz_localize(None)
    return data

data=load_data(selected_stocks)
st.subheader("Raw Data")
st.write(data.tail())


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["date"],y=data["open"],name="stock open"))
    fig.add_trace(go.Scatter(x=data["date"],y=data["close"],name="stock close"))
    fig.layout.update(title_text="Times Series Data",xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data()

df_train=data[["date","close"]]
df_train =df_train.rename(columns={"date":"ds","close":"y"})
m=Prophet()
m.fit(df_train)
future=m.make_future_dataframe(periods=period)
forecast=m.predict(future)

st.subheader("Forecast Data")
st.write(forecast.tail())
st.write("Forecast Data")

fig_fore=plot_plotly(m,forecast, trend=True, changepoints=True)
st.plotly_chart(fig_fore)

fig2=m.plot_components(forecast)
st.write(fig2)
