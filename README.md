# CIFScientists

# Project Title: Analysis of Green House Gases Emitted by America’s 3rd Largest City

This repository is the culmination of a semester long project led by members of Illinois Data Science during the Spring semester of the academic year 2022-2023.

## About This Version

This copy (`idscprojectv2`) is a personal revision maintained by Harshi Vetrivel, built with Claude Code, meant to show both how the analysis itself has evolved since the original 2023 submission and how I work with AI coding tools. It replaces the original 2014-2020 data snapshot with a refreshed 2014-2023 export from the same source, fixes several data-cleaning bugs the original notebook had (see Methodology), extracts that cleaning logic into a tested, reusable module (`clean.py` / `tests/`), and replaces the original grab-bag of exploratory/predictive analyses with a single, more rigorously tested question. The original team and description below are preserved as historical context; the Key Findings, Methodology, and Dataset sections describe the current state of the project.

## Key Findings

**Scope.** These findings are about GHG *intensity* (emissions per square foot) among *buildings represented in Chicago's benchmarking dataset* - large buildings covered by the ordinance, not Chicago's building stock as a whole. This analysis is descriptive: it cannot isolate the ordinance's own effect from other forces (falling efficiency-technology costs, regional/national trends, building-stock turnover) that could produce a similar pattern with or without it, and it says nothing about total emissions, which could still rise even as per-square-foot intensity falls if covered floor area grows.

- **GHG intensity among buildings in the dataset fell from 13.0 to 6.2 kg CO2e/sq ft between 2014 and 2023** - and that decline holds up when checked against a fixed panel of repeat-reporting buildings, arguing against a changing reporting population as the explanation. The 2014 starting point deserves caution, though: Chicago's winter of 2013-14 was its third-coldest on record, which may have inflated 2014's heating-related energy use independent of any efficiency change. Starting the comparison at 2015 instead of 2014 still shows a substantial decline (-38.6% vs. -52.4%), just a smaller one.
- **83.9% of buildings tracked for 4+ years show their own declining GHG intensity trend** (9.6% worsened, 6.6% roughly flat) - not a few large movers doing all the work. This splits unevenly by how much data a building has, though: buildings with only 4-5 years of history show a less favorable split (72.8% improved / 20.1% worsened) than buildings with 8-10 years (89.0% / 5.5%). A confidence-interval check also shows 79.0% of "improved" buildings have a slope statistically distinguishable from zero, versus only 29.6% of "worsened" buildings - the 9.6% worsened figure is closer to an upper bound than a precise count.
- **A dropout check finds modest, mixed evidence of survivorship effects**: buildings that stop reporting before 2023 (18.3% of the panel) show a lower improved share and a higher worsened share than buildings that report throughout, though not a uniformly worse pattern. Not strong enough to say dropout drives the headline number, but not nothing either - see the notebook for the full check and its limits.
- **The decline is front-loaded and partly pandemic-adjacent, not steady, easily-attributed progress**: -36% in 2014-2016 (the period with the weather caveat above), essentially flat in 2016-2019 (-3.6%), a sharp -16% single-year drop in 2020 that coincides with pandemic-driven building vacancy rather than retrofits, then a slower -7.5% crawl through 2023.
- With federal power-plant emissions rules repealed in September 2026, city-level ordinances like Chicago's are increasingly one of the few remaining levers for building-level emissions - this analysis is a look at what the trend actually looks like among covered buildings, not evidence that the ordinance caused it.
- A bonus breakdown by community area shows the fastest-improving areas declining several times faster than the slowest among areas with enough tracked buildings for a stable estimate - descriptive, not causal.
- **A reporting-completeness limitation applies throughout**: 2014-2017 records only ever show `Submitted` status (non-reporters are simply absent as rows); `Not Submitted`/`Exempt` placeholder rows only start appearing around 2018. The scale of non-reporting is measurable for about half the period and invisible for the other half.

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
   - **Has GHG intensity among buildings in Chicago's benchmarking dataset actually declined, or does that just reflect a changing mix of reporting buildings?** Chicago's benchmarking ordinance phased in by building size, so the early reporting pool is a much smaller, different population than the later one. This is checked against a fixed panel of buildings with a multi-year reporting history, not just the raw yearly average.
   - **Among buildings tracked across multiple years, are individual buildings actually reducing their own emissions intensity?** Each repeat-reporting building gets its own year-over-year trend, rather than relying on an aggregate that a changing population or a few large movers could distort.
2. Adds an uncertainty layer to that second question: a standard error on each building's OLS slope (computed with plain numpy, not a new dependency; verified against `scipy.stats.linregress` during development), a breakdown of the improved/flat/worsened split by how many years of data a building has, and a check of how many "improved"/"worsened" slopes are statistically distinguishable from zero. `FLAT_THRESHOLD` itself is unchanged.
3. Checks whether buildings that stop reporting before 2023 look different from buildings that report throughout - a lightweight check on whether panel dropout could be biasing the result, not a claim that it does or doesn't.
4. Breaks the trend into periods rather than accepting the single top-line number, to check whether the decline is steady or concentrated in a few years, and flags that the 2014 baseline may be inflated by an unusually cold winter (see Key Findings).
5. Visualizes the same trend spatially: an animated map (`ghg_intensity_by_year.gif`, reusing the shapefile below) plots every reporting building by location and GHG intensity, one frame per year.
6. Adds a bonus, descriptive breakdown of the per-building trend by community area, using the source data's own labels rather than a hand-built regional grouping - the original's North/South/West lists never covered all of Chicago's community areas, so this version drops that grouping rather than risk repeating the error with a different one.

**What this methodology can't do.** It has no comparison group, so it can't isolate the ordinance's causal effect from other trends moving the same direction. It can't measure buildings outside the benchmarking dataset (small buildings aren't covered). It can't measure non-reporting consistently across the whole period (see the reporting-status limitation above). And it measures per-square-foot intensity, not total emissions.

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

# License

Code in this repository (the notebook, `clean.py`, `tests/`) is available under the [MIT License](LICENSE). The dataset itself is sourced from the [City of Chicago Data Portal](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c) under its own open data terms, not this repository's license.

