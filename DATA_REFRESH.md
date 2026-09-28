# Refreshing the dataset

`Chicago_Energy_Benchmarking.csv` is a manually-exported snapshot, not fetched
by a script. This documents the exact steps used for the September 2026
refresh (2014-2020 -> 2014-2023) so a future refresh doesn't require
re-deriving them from scratch.

## 1. Export from the City of Chicago Data Portal

1. Go to the [Chicago Energy Benchmarking dataset](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c) on the Chicago Data Portal.
2. Use the portal's **Export -> CSV** option (not the Socrata API endpoint -
   the notebook intentionally reads a committed file instead of a live API
   call, so results stay reproducible; see `README.md`).
3. Save the download as `Chicago_Energy_Benchmarking.csv` in the repo root,
   replacing the existing file.

## 2. Know what the export format looks like

The portal's CSV export uses **human-readable column headers** ("Data Year",
"ZIP Code", ...) and formats large numbers with **thousands separators**
(e.g. `"104,849"`), which pandas reads as text, not a number. This is
different from the Socrata API's own CSV endpoint, which returns snake_case
headers and plain numbers - the original 2023 version read from that API
directly and never had to handle either issue.

Both are handled in `clean.py`:
- `COLUMN_RENAME` maps the portal's headers to the API's snake_case names.
- `COMMA_FORMATTED_COLUMNS` lists the columns that need comma-stripping
  before `pd.to_numeric`.

**If the portal changes its export format** (renames a column, changes which
columns are comma-formatted), update those two lists in `clean.py` and run
`pytest tests/` - `test_columns_are_renamed_to_snake_case` and
`test_comma_formatted_numbers_are_coerced_to_numeric` will fail if a mapping
is now stale, before it silently produces wrong numbers downstream (as it did
with the original 2023 notebook: see the "What Actually Running the Code
Found" section of `OVERVIEW.pdf`).

## 3. Re-run and verify

```
pytest tests/                      # confirm the cleaning pipeline still holds
jupyter lab Chicago_Energy.ipynb   # Run All, check for errors
```

Re-running the notebook regenerates `ghg_intensity_by_year.gif` in place.
Check the printed cell outputs against expectations before committing:
row count, `data_year` range, and the panel-building count should all grow
with a newer export; the shape of the year-over-year trend numbers is worth
sanity-checking against the previous refresh's numbers in `README.md`'s Key
Findings, since a large unexplained jump usually means something upstream
changed (a portal schema change, a data correction, etc.) rather than a
genuine trend shift.
