import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def predict_future_prices(market_prices, dates):
    dates_numeric = (pd.to_datetime(dates) - pd.to_datetime(dates).min()).dt.days.values.reshape(-1, 1)
    market_prices_numeric = np.array(market_prices).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(dates_numeric, market_prices_numeric)
    
    # Predict future prices (for example, next 30 days)
    future_dates = np.arange(dates_numeric[-1] + 1, dates_numeric[-1] + 31).reshape(-1, 1)
    future_prices = model.predict(future_dates)
    
    # Slope and intercept of the regression line
    slope, intercept = model.coef_[0][0], model.intercept_[0]
    
    return future_dates, future_prices, slope, intercept


market_data = pd.read_csv('./data/market_row_csv.csv')
filtered_data = market_data[(market_data['origin'] == 'SGSIN') & (market_data['destination'] == 'USLAX')]
print(market_data.head())

future_dates, future_prices, slope, intercept = predict_future_prices(filtered_data['price'], 
                                                                      filtered_data['date'])

print("Future Dates:", future_dates)
print("Future Prices:", future_prices)
print("Slope:", slope)
print("Intercept:", intercept)