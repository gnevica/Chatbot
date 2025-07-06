from prophet import Prophet
import pandas as pd
import plotly.express as px

def forecast_with_prophet(df, user_query):
    date_col = df.columns[0]
    value_col = df.columns[1]
    df = df.rename(columns={date_col: 'ds', value_col: 'y'})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=12, freq='M')
    forecast = model.predict(future)
    fig = px.line(forecast, x='ds', y='yhat', title='Forecast')
    return fig