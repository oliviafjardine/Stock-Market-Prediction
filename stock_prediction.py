import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot

API_KEY = '98Q36G3NSQ7PHLPO'
symbol = 'NVDA'

# Alpha Vantage API URL
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&datatype=csv&apikey={API_KEY}'

# Download CSV data
response = requests.get(url)
if response.status_code == 200:
    with open('stock_data.csv', 'w') as f:
        f.write(response.text)
    print("Stock data saved to stock_data.csv")
else:
    print("Failed to fetch stock data. Check your API key or symbol.")
    exit()

# Load the CSV data
nvidia = pd.read_csv('stock_data.csv')

# Inspect the column names to ensure correct mapping
print("Columns in the DataFrame:", nvidia.columns)

# Rename columns for consistency (if necessary)
nvidia.rename(
    columns={
        'timestamp': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume',
    },
    inplace=True,
    errors='ignore'
)

# Sort by date
nvidia['Date'] = pd.to_datetime(nvidia['Date'])
nvidia.sort_values('Date', inplace=True)

print(f'Dataframe contains stock prices between {nvidia.Date.min()} and {nvidia.Date.max()}')
print(f'Total Days = {(nvidia.Date.max() - nvidia.Date.min()).days} days')

# Check data
print(nvidia.describe())

# Box plot for Open, High, Low, Close
try:
    nvidia[['Open', 'High', 'Low', 'Close']].plot(kind='box', figsize=(10, 6), title="Box Plot of Stock Prices")
    plt.show()
except KeyError as e:
    print("Column names are missing or incorrect. Check the DataFrame's columns:", e)

# Set layout for Plotly plot
layout = go.Layout(
    title='Stock Prices of Nvidia',
    xaxis=dict(
        title=dict(
            text='Date',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=dict(
        title=dict(
            text='Price',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
)

# Create Plotly data
nvidia_data = [go.Scatter(x=nvidia['Date'], y=nvidia['Close'], mode='lines', name='Closing Price')]
fig = go.Figure(data=nvidia_data, layout=layout)
plot(fig, filename='nvidia_stock_prices.html')  # Save and open the plot in a browser

# Use closing price for prediction
nvidia['Close'] = pd.to_numeric(nvidia['Close'], errors='coerce')

# Drop rows with NaN values in 'Close'
nvidia.dropna(subset=['Close'], inplace=True)

# Optional: limit to last N days
nvidia = nvidia.tail(365)

# Matplotlib Plotting for Closing Prices
plt.figure(figsize=(10, 5))
plt.plot(nvidia['Date'], nvidia['Close'], label='Closing Price')
plt.title('NVIDIA Stock Prices - Last 365 Days')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.grid(True)
plt.show()