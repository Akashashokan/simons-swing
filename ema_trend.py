import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime, timedelta

def check_ema_trend(data):
    # Sort DataFrame by date in ascending order
    data = data.sort_values(by='Date')

    # Calculate EMAs
    data['EMA_40'] = data['Close'].ewm(span=40, adjust=False).mean()
    data['EMA_120'] = data['Close'].ewm(span=120, adjust=False).mean()
    data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()

    # Filter data for the last 6 months
    six_months_ago = datetime.now() - timedelta(days=180)
    data_last_six_months = data[data['Date'] >= six_months_ago]

    # Perform regression analysis
    def calculate_slope(x, y):
        x = sm.add_constant(x)
        model = sm.OLS(y, x)
        results = model.fit()
        return results.params[1]

    # Calculate slope for each EMA
    slope_40 = calculate_slope(np.arange(len(data_last_six_months)), data_last_six_months['EMA_40'])
    slope_120 = calculate_slope(np.arange(len(data_last_six_months)), data_last_six_months['EMA_120'])
    slope_200 = calculate_slope(np.arange(len(data_last_six_months)), data_last_six_months['EMA_200'])

    print(slope_40,slope_120,slope_200)
    # Analyze the slopes
    if slope_40 > 0 and slope_120 > 0 and slope_200 > 0:
        return "EMAs are in an upward direction for the last 6 months."
    elif slope_40 == 0 and slope_120 == 0 and slope_200 == 0:
        return "EMAs are flat for the last 6 months."
    else:
        return "EMAs are not consistently in an upward direction for the last 6 months."
