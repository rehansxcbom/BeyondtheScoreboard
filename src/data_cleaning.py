"""Data quality checks and cleaning pipeline for the raw dataset tables."""

import pandas as pd


def clean_columns(df):
    """Standardise column names to snake_case."""
    out = df.copy()
    out.columns = (
        out.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return out


def clean_all(raw):
    """Standardise columns, drop duplicates and handle known missing-value cases.

    Returns (data, quality_report) where `data` is the cleaned table dict and
    `quality_report` is a DataFrame summarising rows/columns/missing/duplicates
    per table.
    """
    data = {name: clean_columns(df) for name, df in raw.items()}

    duplicate_report = {}
    for name, df in data.items():
        duplicate_report[name] = int(df.duplicated().sum())
        data[name] = df.drop_duplicates().copy()

    # Drop player-stat columns that carry no observations at all.
    player_drop = [
        c for c in ["shots", "shots_on_target", "average_rating"]
        if c in data["player_stats"].columns and data["player_stats"][c].isna().all()
    ]
    data["player_stats"] = data["player_stats"].drop(columns=player_drop)

    if "data_source" in data["player_stats"].columns:
        data["player_stats"]["data_source"] = data["player_stats"]["data_source"].fillna("Unknown")

    # Trim whitespace on all text columns.
    for name, df in data.items():
        text_cols = df.select_dtypes(include="object").columns
        for c in text_cols:
            df[c] = df[c].str.strip()

    quality_rows = []
    for name, df in data.items():
        quality_rows.append({
            "Dataset": name,
            "Rows": len(df),
            "Columns": df.shape[1],
            "Missing cells": int(df.isna().sum().sum()),
            "Duplicate rows removed": duplicate_report[name],
        })
    quality_report = pd.DataFrame(quality_rows)

    print("Data cleaning pipeline complete.")
    print("Dropped columns due to absolute null bounds:", player_drop)

    return data, quality_report