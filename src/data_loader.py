"""Locate, extract and load the raw FIFA World Cup 2026 dataset tables."""

import os
import glob
import zipfile

import pandas as pd

TABLE_FILES = {
    "teams": "teams.csv",
    "matches": "matches.csv",
    "matches_detailed": "matches_detailed.csv",
    "match_team_stats": "match_team_stats.csv",
    "player_stats": "player_stats.csv",
    "squads_players": "squads_and_players.csv",
    "match_events": "match_events.csv",
    "tournament_stages": "tournament_stages.csv",
}


def locate_zip(search_dirs=(".",)):
    """Find the dataset zip archive in the given search directories."""
    candidates = []
    for folder in search_dirs:
        if os.path.exists(folder):
            candidates.extend(glob.glob(os.path.join(folder, "*.zip")))
    fifa = [
        p for p in candidates
        if "FIFA" in os.path.basename(p) or "World-Cup" in os.path.basename(p)
    ]
    return sorted(fifa)[0] if fifa else (sorted(candidates)[0] if candidates else None)


def extract_dataset(zip_path, extract_dir="./fifa_wc_2026_data"):
    """Extract the dataset zip and return the directory containing the CSVs."""
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    teams_file = next(iter(glob.glob(os.path.join(extract_dir, "**", "teams.csv"), recursive=True)), None)
    if teams_file is None:
        raise FileNotFoundError("The file 'teams.csv' could not be found within the extracted directory path.")
    return os.path.dirname(teams_file)


def load_csv(repo_root, filename):
    path = next(iter(glob.glob(os.path.join(repo_root, "**", filename), recursive=True)), None)
    if path is None:
        raise FileNotFoundError(f"Required table '{filename}' is missing from the data repository.")
    return pd.read_csv(path)


def load_all_tables(search_dirs=(".", "/content", "/mnt/data")):
    """Locate the dataset zip, extract it and load every raw table."""
    zip_path = locate_zip(search_dirs)
    if zip_path is None:
        raise FileNotFoundError(
            "Dataset archive ZIP not found. Please place the dataset zip in the project root."
        )
    print("Target archive recognized:", zip_path)

    repo_root = extract_dataset(zip_path)
    raw = {name: load_csv(repo_root, filename) for name, filename in TABLE_FILES.items()}

    for name, df in raw.items():
        print(f"Loaded DataFrame: {name:20s} Dimension Matrix: {df.shape}")

    return raw