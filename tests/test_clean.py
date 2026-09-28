"""Tests for clean.py.

Unit tests run against a small synthetic fixture (tests/fixtures/sample_export.csv)
built to exercise each cleaning step. One integration test runs the same
pipeline against the real committed dataset, so a future data refresh that
breaks an assumption (e.g. a renamed column, a new duplicate) fails loudly
here instead of silently in the notebook.
"""

import os

import pandas as pd
import pytest

import clean

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
SAMPLE_CSV = os.path.join(FIXTURES_DIR, "sample_export.csv")
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
REAL_CSV = os.path.join(REPO_ROOT, "Chicago_Energy_Benchmarking.csv")


@pytest.fixture
def sample_df():
    return clean.load_and_clean(SAMPLE_CSV)


def test_columns_are_renamed_to_snake_case(sample_df):
    assert "community_area" in sample_df.columns
    assert "gross_floor_area_buildings_sq_ft" in sample_df.columns
    assert "Community Area" not in sample_df.columns


def test_comma_formatted_numbers_are_coerced_to_numeric(sample_df):
    for col in clean.COMMA_FORMATTED_COLUMNS:
        assert pd.api.types.is_numeric_dtype(sample_df[col]), f"{col} is not numeric"
    tower_a = sample_df.loc[sample_df["id"] == 100001].iloc[0]
    assert tower_a["gross_floor_area_buildings_sq_ft"] == 64028
    assert tower_a["electricity_use_kbtu"] == pytest.approx(2384738.9)


def test_rows_with_no_community_area_are_dropped(sample_df):
    # Tower C has no Community Area in the fixture and should be dropped.
    assert 100003 not in sample_df["id"].values
    assert sample_df["community_area"].isna().sum() == 0


def test_community_area_is_title_cased_and_ohare_is_fixed(sample_df):
    areas = set(sample_df["community_area"])
    assert "Hyde Park" in areas  # was "HYDE PARK"
    assert "Near West Side" in areas  # was "near west side"
    assert "O'Hare" in areas  # was "Ohare"
    assert "Ohare" not in areas


@pytest.mark.skipif(not os.path.exists(REAL_CSV), reason="real dataset not present")
def test_real_dataset_has_no_duplicate_building_year_records():
    df = clean.load_and_clean(REAL_CSV)
    duplicates = df.duplicated(subset=["id", "data_year"]).sum()
    assert duplicates == 0


@pytest.mark.skipif(not os.path.exists(REAL_CSV), reason="real dataset not present")
def test_real_dataset_ghg_intensity_is_never_negative():
    df = clean.load_and_clean(REAL_CSV)
    non_null = df["ghg_intensity_kg_co2e_sq_ft"].dropna()
    assert (non_null >= 0).all()
