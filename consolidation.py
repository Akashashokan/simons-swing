import pandas as pd

def check_price_consolidation(data):
    # Calculate 52-week high
    high_52_weeks = data['High'].rolling(window=200, min_periods=1).max()
    
    # Calculate the range of 25% of the 52-week high
    twenty_five_percent_range = 0.30 * high_52_weeks
    
    # Calculate lower and upper bounds for consolidation box
    lower_bound = high_52_weeks - twenty_five_percent_range
    # upper_bound = high_52_weeks + twenty_five_percent_range
    upper_bound = high_52_weeks

    # Check for consolidation for at least 20 days within the range
    consolidation_mask = (data['High'] <= upper_bound) & (data['Low'] >= lower_bound)
    consolidated_days = consolidation_mask.rolling(window=15).sum() >= 15
    
    # Check for lower volume
    # lower_volume_mask = data['Volume'].rolling(window=20).mean() < data['Volume'].rolling(window=100).mean()
    
    # Check if the final candle is breaking out of the upper range with higher volume
    final_candle_breakout = (data['Close'] > upper_bound.shift(-1)) & (data['Volume'] > data['Volume'].rolling(window=2).mean())
    
    # return consolidated_days & lower_volume_mask & final_candle_breakout
    return consolidated_days  & final_candle_breakout
