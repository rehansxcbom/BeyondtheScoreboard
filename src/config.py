"""Environment configuration for the FIFA World Cup 2026 analysis pipeline."""

import warnings
import pandas as pd


def configure_environment():
    """Apply global pandas/warnings settings used throughout the analysis."""
    warnings.filterwarnings("ignore")
    pd.set_option("display.max_columns", 100)
    pd.set_option("display.float_format", lambda x: f"{x:,.3f}")
    print("Environment configured. Ready for data ingestion.")