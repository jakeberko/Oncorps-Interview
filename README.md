# Pass/Fail Check Pipeline

Ingests historical daily closing prices for US stock indexes and flags
day-over-day and week-over-week moves that break configurable thresholds.

## Run it

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
```

Results are written to `output/results.csv` with columns: `ticker`,
`date_from`, `date_to`, `value_from`, `value_to`, `pct_change`.

## Config

Thresholds and on/off switches live in `config.yaml`. Each index can
override the global defaults (see SP500's `daily_threshold_pct: 1.5`).

## Data

`data/` contains daily closing values for SP500, DJIA, and NASDAQCOM,
sourced from FRED (`observation_date,<TICKER>` format).

## Notes

- Week-over-week comparisons are non-overlapping: once a breach window is
  checked, the pointer advances past it rather than sliding day-by-day.
  This means not every day gets a weekly comparison, only every ~7 days.
- Static YAML config was chosen over a DB-backed approach since the check
  universe (a handful of indexes) is small and infrequently changed — a
  file keeps the pipeline version-controlled and zero-infrastructure.

## AI assistance disclosure

Parts of this project (scaffolding, code, and this README) were drafted
with AI assistance. All code has been reviewed and can be explained and
modified live without AI help.