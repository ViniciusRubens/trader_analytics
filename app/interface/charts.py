import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class StockVisualizer:
    """
    Class responsible for generating and rendering interactive stock market 
    charts using Plotly and Streamlit.
    """

    def __init__(self):
        """
        Initializes the visualizer. 
        Future visual configurations (like custom themes or color palettes) 
        can be set up here.
        """
        pass

    def plot_stock_price(self, hist: pd.DataFrame, ticker: str):
        """
        Plots a line chart showing the closing price of the stock.
        """
        fig = px.line(
            hist, 
            x = "Date", 
            y = "Close", 
            title = f"{ticker} Stock Price (Last 6 Months)", 
            markers = True
        )
        st.plotly_chart(fig, use_container_width = True)

    def plot_candlestick(self, hist: pd.DataFrame, ticker: str):
        """
        Plots a candlestick chart showing Open, High, Low, and Close prices.
        """
        fig = go.Figure(
            data = [go.Candlestick(
                x = hist['Date'],
                open = hist['Open'],
                high = hist['High'],
                low = hist['Low'],
                close = hist['Close']
            )]
        )
        fig.update_layout(title = f"{ticker} Candlestick Chart (Last 6 Months)")
        st.plotly_chart(fig, use_container_width = True)

    def plot_moving_averages(self, hist: pd.DataFrame, ticker: str):
        """
        Calculates and plots the 20-day Simple Moving Average (SMA) 
        and Exponential Moving Average (EMA) alongside the closing price.
        """
        # Create a copy to avoid SettingWithCopyWarning on the original DataFrame
        data = hist.copy()
        
        # Calculate Simple Moving Average (SMA) - 20 periods
        data['SMA_20'] = data['Close'].rolling(window = 20).mean()
        
        # Calculate Exponential Moving Average (EMA) - 20 periods
        data['EMA_20'] = data['Close'].ewm(span = 20, adjust = False).mean()
        
        fig = px.line(
            data, 
            x = 'Date', 
            y = ['Close', 'SMA_20', 'EMA_20'],
            title = f"{ticker} Moving Averages (Last 6 Months)",
            labels = {'value': 'Price (USD)', 'Date': 'Date'}
        )
        st.plotly_chart(fig, use_container_width = True)

    def plot_volume(self, hist: pd.DataFrame, ticker: str):
        """
        Plots a bar chart showing the trading volume over time.
        """
        fig = px.bar(
            hist, 
            x = 'Date', 
            y = 'Volume', 
            title = f"{ticker} Trading Volume (Last 6 Months)"
        )
        st.plotly_chart(fig, use_container_width = True)