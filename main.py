# pyright: basic
import datetime
from pathlib import Path

import pandas as pd


def unique_ids(data):
    players_ids = data["playerId"].unique()
    return players_ids


def number_of_players(data):
    return unique_ids(data).size


def get_ages(data):
    get_mm_dd_yyyy = lambda s: s.split("(")[0].strip()
    date_of_birth = data["birthdate"].map(get_mm_dd_yyyy)
    date_of_birth_sanitized = pd.to_datetime(
        date_of_birth, format="%m/%d/%Y", errors="coerce"
    )
    age = pd.to_datetime("now") - date_of_birth_sanitized
    return age


if __name__ == "__main__":
    data = pd.read_csv(Path("nba_stats.csv"))
    print(unique_ids(data))
    print(number_of_players(data))
    print(get_ages(data))
