# CIFScientists

# Project Title: Analysis of Green House Gases Emitted by America’s 3rd Largest City

This repository is the culmination of a semester long project led by members of Illinois Data Science during the Spring semester of the academic year 2022-2023.

## About This Version

This copy (`idscprojectv2`) is a personal revision maintained by Harshi Vetrivel, built with Claude Code, meant to show both how the analysis itself has evolved since the original 2023 submission and how I work with AI coding tools. It replaces the original 2014-2020 data snapshot with a refreshed 2014-2023 export from the same source, fixes several data-cleaning bugs the original notebook had (see Methodology), extracts that cleaning logic into a tested, reusable module (`clean.py` / `tests/`), and replaces the original grab-bag of exploratory/predictive analyses with a single, more rigorously tested question. The original team and description below are preserved as historical context; the Key Findings, Methodology, and Dataset sections describe the current state of the project.

## Key Findings

- **Citywide GHG intensity fell from 13.0 to 6.2 kg CO2e/sq ft between 2014 and 2023** - and that decline holds up when checked against a fixed panel of repeat-reporting buildings, arguing against a changing reporting population as the explanation.
- **83.9% of buildings tracked for 4+ years show their own declining GHG intensity trend** (9.6% worsened, 6.6% roughly flat) - the citywide number isn't hiding a few large movers doing all the work.
- **The decline is front-loaded and partly pandemic-adjacent, not steady policy-driven progress**: -36% in 2014-2016, essentially flat in 2016-2019 (-3.6%), a sharp -16% single-year drop in 2020 that coincides with pandemic-driven building vacancy rather than retrofits, then a slower -7.5% crawl through 2023.
- With federal power-plant emissions rules repealed in September 2026, city-level ordinances like Chicago's are increasingly the primary lever left for building decarbonization - this analysis is a check on how well that lever has actually performed, not just whether it exists.
- A bonus breakdown by community area shows the fastest-improving areas declining several times faster than the slowest among areas with enough tracked buildings for a stable estimate - descriptive, not causal.

A 14-slide summary of these findings is in `OVERVIEW.pdf`.

# Meet our Team:

Denise Bahena -  Co-Team Lead

Alekhya Nathella - Co-Team Lead 

Otniel Fernandez - Collaborator

Ryan Oh - Collaborator

Claire Quin - Collaborator

Claudia Robles - Collaborator

Harshi Vetrivel - Collaborator


# Official Description:

In an effort to stave off the environmental crisis that is predicted to occur later this century, many 
cities have begun to implement policies with the objective of reducing the ecological impact that urban places have on the environment due to their advanced industrialization. Thus, our goal is to analyze the energy program of one such city, Chicago, Illinois, to measure the success of their efforts as a whole, and locate any other trends regarding energy use in the city.

The technical tools used to complete this analysis are:
Python — Programming Language
Colab — Web IDE, for ease of collaboration

Packages used to complete analysis are:
Pandas — Data Analysis
Numpy — Number manipulation
Matplotlib.pyplot — Data Visualization

# Running This Analysis

```
pip install -r requirements.txt
pytest tests/            # verify the cleaning pipeline against real + synthetic data
jupyter lab Chicago_Energy.ipynb   # or open in VS Code / Colab, then Run All
```

The notebook expects `Chicago_Energy_Benchmarking.csv` and the `chicago_outline.*` shapefiles in the same directory (both already committed here) and imports `clean.py` from that directory too - run Jupyter from the repo root.

# Methodology

Data cleaning lives in `clean.py` (covered by `tests/test_clean.py`), not inline in the notebook: it renames the portal export's human-readable column headers to the snake_case field names the API version uses, coerces the numeric columns the export formats with thousands separators (e.g. `"104,849"`) back to numeric, and drops/normalizes rows with no community area. `Chicago_Energy.ipynb` calls that module, runs an upfront missing-values and duplicate-`(id, data_year)` audit, and then:

1. Answers two questions the original single-snapshot version couldn't, now that the dataset spans 10 years (2014-2023):
   - **Has citywide GHG intensity actually declined, or does that just reflect a changing mix of reporting buildings?** Chicago's benchmarking ordinance phased in by building size, so the early reporting pool is a much smaller, different population than the later one. This is checked against a fixed panel of buildings with a multi-year reporting history, not just the raw yearly average.
   - **Among buildings tracked across multiple years, are individual buildings actually reducing their own emissions intensity?** Each repeat-reporting building gets its own year-over-year trend, rather than relying on a citywide average that a changing population or a few large movers could distort.
2. Breaks the citywide trend into periods rather than accepting the single top-line number, to check whether the decline is steady or concentrated in a few years (see Key Findings).
3. Visualizes the same trend spatially: an animated map (`ghg_intensity_by_year.gif`, reusing the shapefile below) plots every reporting building by location and GHG intensity, one frame per year.
4. Adds a bonus, descriptive breakdown of the per-building trend by community area, using the source data's own labels rather than a hand-built regional grouping - the original's North/South/West lists never covered all of Chicago's community areas, so this version drops that grouping rather than risk repeating the error with a different one.

The original 2023 version instead asked whether GHG emissions were linearly associated with electricity use and square footage, and whether mean GHG intensity differed significantly across building types, using regression, a building-size classifier (Random Forest / KNN), and a hand-built North/South/West community-area grouping that never covered all of Chicago's community areas. That analysis has been removed from this version in favor of the trend analysis above; it's still available in this repository's git history.

# Dataset: Chicago Energy Benchmarking, 2014-2023

Chicago Energy Benchmarking (CSV) sourced through: City of Chicago Data Portal. Refreshed September 2026 from the same source as the original project; replaces the original 2014-2020 snapshot (17,728 rows) with a 2014-2023 export (28,329 rows). See `DATA_REFRESH.md` for the exact steps to refresh it again.

Chicago Outline shape files: originally used by the 2023 version's Geopandas map, then unused for a time when that section was cut; reused in this version by the animated GHG-intensity map (`ghg_intensity_by_year.gif`).

# Data Dictionary

Data Year: Calendar Year of every record

ID: A six digit unique identifier assigned to each property by the Chicago Energy Benchmarking Ordinance

Property Name: Official name of the property

Reporting Status: If the property submitted a report for that calendar year

Address: Street Address of the property

Zip Code: Zip Code of the property

Chicago Energy Rating: Zero to four star energy rating assigned to each property

Exempt from Chicago Energy Rating: Shows if the property is subject to the Chicago Energy Benchmarking Ordinance

Community Area: The Chicago community Area where the property is located

Primary Property Type: the primary function of a property

Gross Floor Area: The total indoor area of the property in square feet

Year Built: The year the property was built

Number of buildings: Number of buildings in the property

Water Use: Water use per year in thousands of gallons

Energy Star Score: Rating of property’s overall energy score out of 100

Electricity Use: Annual Electricity use in thousands of British Thermal Unit

Natural Gas Use: Annual Natural Gas use in thousands of British Thermal Unit

District Steam Use: Annual District Steam use in thousands of British Thermal Unit

District Chilled Water Use: Annual District Chilled Water use in thousands of British Thermal Unit

All Other Fuel Use: Annual Other Fuel use in thousands of British Thermal Unit

Site EUI: Site Energy Use Intensity is the energy use divided by the gross floor area 

Source EUI: Source Energy Use, Annual energy use to operate divided by the area in square feet

Weather Normalized Site EUI: Site Energy Use Intensity during 30-year average weather conditions

Weather Normalized Source EUI: Source Energy Use Intensity during 30-year average weather conditions

Total GHG Emissions: Total greenhouse gas emissions of carbon dioxide, methane and nitrous oxide in metric tons

GHG Intensity: Total GHG Emissions divided per square foot

Latitude: Latitude of the property

Longitude: Longitude of the property

Location: Latitude and longitude of the property

