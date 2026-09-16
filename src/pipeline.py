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
        
prices = load_prices("data/DJIA.csv", "observation_date", "DJIA")
print(len(prices))
print(type(prices[0][1])) 