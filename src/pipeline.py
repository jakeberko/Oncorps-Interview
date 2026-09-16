import csv
from datetime import datetime
from datetime import timedelta
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

def wow_check(ticker, prices, threshold):
    breaches = []
    ptr = 0
    for i, curr in enumerate(prices):
        curr_date, curr_val = curr
        if (curr_date - prices[ptr][0]) < timedelta(days=7): 
            continue

        prev_date, prev_val = prices[ptr]
        pct_change = (curr_val - prev_val) / prev_val * 100
        
        if abs(pct_change) > threshold:
            breach_dict = {
                "ticker": ticker,
                "date_from": prev_date,
                "date_to": curr_date,
                "value_from": prev_val,
                "value_to": curr_val,
                "pct_change": pct_change,
            }
            breaches.append(breach_dict)
        ptr = i
    return breaches

def resolve_check_settings(index_cfg, defaults_cfg):
    daily_enabled = index_cfg.get("daily_enabled", defaults_cfg["checks"]["day_over_day"]["enabled"])
    daily_threshold = index_cfg.get("daily_threshold_pct", defaults_cfg["checks"]["day_over_day"]["threshold_pct"])
    weekly_enabled = index_cfg.get("weekly_enabled", defaults_cfg["checks"]["week_over_week"]["enabled"])
    weekly_threshold = index_cfg.get("weekly_threshold_pct", defaults_cfg["checks"]["week_over_week"]["threshold_pct"])
    return daily_enabled, daily_threshold, weekly_enabled, weekly_threshold

def write_results(breaches, output_path):
    fieldnames = ["ticker", "date_from", "date_to", "value_from", "value_to", "pct_change"]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(breaches)

def run_pipeline(config_path, output_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    all_breaches = []

    for index_cfg in config["indexes"]:
        ticker = index_cfg["ticker"]
        prices = load_prices(index_cfg["file"], index_cfg["date_column"], index_cfg["value_column"])
        daily_enabled, daily_threshold, weekly_enabled, weekly_threshold = resolve_check_settings(index_cfg, config["defaults"])

        # .extend() adds each breach dict individually .append() nests the whole list as one element
        if daily_enabled:
            all_breaches.extend(dod_check(ticker, prices, daily_threshold))
        if weekly_enabled:
            all_breaches.extend(wow_check(ticker, prices, weekly_threshold))

    write_results(all_breaches, output_path)


if __name__ == "__main__":
    run_pipeline("config.yaml", "output/results.csv")