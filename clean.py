"""Load and clean the Chicago Energy Benchmarking dataset.

Extracted from the notebook so the cleaning logic is testable and reusable
independent of the analysis that consumes it.
"""

import pandas as pd

# The City of Chicago Data Portal's CSV export uses human-readable column
# headers. This renames them to the snake_case field names the portal's own
# Socrata API returns, since the analysis (and the original 2023 version,
# which loaded data straight from that API) is written against those names.
COLUMN_RENAME = {
    "Data Year": "data_year",
    "ID": "id",
    "Property Name": "property_name",
    "Reporting Status": "reporting_status",
    "Address": "address",
    "ZIP Code": "zip_code",
    "Chicago Energy Rating": "chicago_energy_rating",
    "Exempt From Chicago Energy Rating": "exempt_from_chicago_energy_rating",
    "Community Area": "community_area",
    "Primary Property Type": "primary_property_type",
    "Gross Floor Area - Buildings (sq ft)": "gross_floor_area_buildings_sq_ft",
    "Year Built": "year_built",
    "# of Buildings": "number_of_buildings",
    "Water Use (kGal)": "water_use_kgal",
    "ENERGY STAR Score": "energy_star_score",
    "Electricity Use (kBtu)": "electricity_use_kbtu",
    "Natural Gas Use (kBtu)": "natural_gas_use_kbtu",
    "District Steam Use (kBtu)": "district_steam_use_kbtu",
    "District Chilled Water Use (kBtu)": "district_chilled_water_use_kbtu",
    "All Other Fuel Use (kBtu)": "all_other_fuel_use_kbtu",
    "Site EUI (kBtu/sq ft)": "site_eui_kbtu_sq_ft",
    "Source EUI (kBtu/sq ft)": "source_eui_kbtu_sq_ft",
    "Weather Normalized Site EUI (kBtu/sq ft)": "weather_normalized_site_eui_kbtu_sq_ft",
    "Weather Normalized Source EUI (kBtu/sq ft)": "weather_normalized_source_eui_kbtu_sq_ft",
    "Total GHG Emissions (Metric Tons CO2e)": "total_ghg_emissions_metric_tons_co2e",
    "GHG Intensity (kg CO2e/sq ft)": "ghg_intensity_kg_co2e_sq_ft",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Location": "location",
    "Row_ID": "row_id",
}

# The portal export formats large numbers with thousands separators
# (e.g. "104,849"), which pandas reads as text rather than a number.
COMMA_FORMATTED_COLUMNS = [
    "gross_floor_area_buildings_sq_ft",
    "water_use_kgal",
    "electricity_use_kbtu",
    "natural_gas_use_kbtu",
    "district_steam_use_kbtu",
    "district_chilled_water_use_kbtu",
    "all_other_fuel_use_kbtu",
    "site_eui_kbtu_sq_ft",
    "source_eui_kbtu_sq_ft",
    "weather_normalized_site_eui_kbtu_sq_ft",
    "weather_normalized_source_eui_kbtu_sq_ft",
    "total_ghg_emissions_metric_tons_co2e",
]


def load_raw(csv_path: str) -> pd.DataFrame:
    """Read the portal export and rename its columns to snake_case."""
    df = pd.read_csv(csv_path)
    return df.rename(columns=COLUMN_RENAME)


def coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip thousands separators and coerce the affected columns to numeric."""
    df = df.copy()
    for col in COMMA_FORMATTED_COLUMNS:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
    return df


def clean_community_area(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with no community area, and normalize spelling/casing."""
    df = df.dropna(subset=["community_area"]).reset_index(drop=True)
    df["community_area"] = df["community_area"].str.title()
    df["community_area"] = df["community_area"].replace("Ohare", "O'Hare")
    return df


def load_and_clean(csv_path: str) -> pd.DataFrame:
    """Load the portal export and apply the full cleaning pipeline."""
    df = load_raw(csv_path)
    df = coerce_numeric_columns(df)
    df = clean_community_area(df)
    return df
