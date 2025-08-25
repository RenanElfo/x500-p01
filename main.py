# pyright: basic
import datetime
from pathlib import Path

import pandas as pd

AVARAGE_DAYS_IN_A_YEAR = 365.2425

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
    year = pd.to_datetime(data["year"], format="%Y")
    age = (year - date_of_birth_sanitized).map(
        lambda time_delta: int(time_delta.days // AVARAGE_DAYS_IN_A_YEAR)
    )
    return age


if __name__ == "__main__":
    data = pd.read_csv(Path("nba_stats.csv"))
    relevant_information = pd.concat(
        [data["playerId"].to_frame().T, get_ages(data).to_frame().T]
    ).T
    print(relevant_information)
    print(unique_ids(data))
    print(number_of_players(data))
    print(get_ages(data))
