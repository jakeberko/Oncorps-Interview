import csv
from datetime import datetime
import yaml

def load_prices(filepath, date_col, value_col):
    prices = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[value_col] not in ("", "."):
                date = datetime.fromisoformat(row[date_col])
                val = float(row[value_col])
                prices.append((date,val))
    prices.sort()
    return prices

def dod_check(ticker, prices, threshold):
    breaches = []
    for prev, curr in zip(prices, prices[1:]):
        if prev[1] == 0: continue

        prev_val, curr_val = prev[1], curr[1]
        pct_change = (curr_val - prev_val) / prev_val * 100
        
        if abs(pct_change) > threshold:
          prev_date, curr_date = prev[0], curr[0]
          breach_dict = {
              "ticker": ticker,
              "date_from": prev_date,
              "date_to": curr_date,
              "value_from": prev_val,
              "value_to": curr_val,
              "pct_change": pct_change,
            }
          breaches.append(breach_dict)
    return breaches

prices = load_prices("data/DJIA.csv", "observation_date", "DJIA")
print(len(prices))
print(type(prices[0][1])) 

result = dod_check("DJIA", load_prices("data/DJIA.csv", "observation_date", "DJIA"), 1.0)
print(len(result))
print(result[0])