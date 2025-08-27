# pyright: basic
from pathlib import Path

import pandas as pd
import numpy as np

DATA_PATH = Path("nba_stats.csv")
AVARAGE_DAYS_IN_A_YEAR = 365.2425
FEET_TO_CENTIMETER = 30.48
INCHES_TO_CENTIMETER = 2.54
POUNDS_TO_KILOGRAMS = 0.4535924
INFO_TO_CONSIDER = [
    "year",
    "playerId",
    "positionId",
    "gamesPlayed",
    "doubleDouble",
    "tripleDouble",
    "minutes",
    "rebounds",
    "fieldGoalPct",
    "threePointFieldGoalPct",
    "freeThrowPct",
    "points",
    "assists",
    "turnovers",
    "steals",
    "blocks",
    "birthdate",
    "htwt",
    "salary",
]
INFO_TO_AVERAGE_PER_MATCH = [
    "doubleDouble",
    "tripleDouble"
]
INFO_TO_AVERAGE_PER_MINUTE = [
    "rebounds",
    "points",
    "assists",
    "turnovers",
    "steals",
    "blocks",
]
NON_METRIC_INFO = [
    "year",
    "playerId",
    "positionId",
    "birthdate",
    "htwt",
]

def parse_and_replace_salary(data: pd.DataFrame) -> pd.DataFrame:
    parse_salary = lambda s: float(s[1:].replace(",", ""))
    salary = pd.Series(data["salary"].map(parse_salary))
    data.drop("salary", axis=1, inplace=True)
    data.insert(data.columns.size, "salary", salary) 
    return data


def get_average_double_double(data: pd.DataFrame):
    games_played = data["gamesPlayed"]
    double_double = data["doubleDouble"]
    average_double_double = double_double / games_played
    return average_double_double.rename("avgDoubleDouble")

def get_average_triple_double(data: pd.DataFrame):
    games_played = data["gamesPlayed"]
    triple_double = data["tripleDouble"]
    average_triple_double = triple_double / games_played
    return average_triple_double.rename("avgTripleDouble")

def get_points_per_minute(data: pd.DataFrame):
    return (data["points"] / data["minutes"]).rename("pointsPerMinute")


def number_of_players(data):
    players_ids = data["playerId"].unique()
    return players_ids.size


def get_player_ids(data: pd.DataFrame) -> pd.Series:
    return pd.Series(data["playerId"])


def get_and_replace_age(data) -> pd.DataFrame:
    get_mm_dd_yyyy = lambda s: s.split("(")[0].strip()
    date_of_birth = data["birthdate"].map(get_mm_dd_yyyy)
    date_of_birth_sanitized = pd.to_datetime(
        date_of_birth, format="%m/%d/%Y", errors="coerce"
    )
    year = pd.to_datetime(data["year"], format="%Y")
    age = (year - date_of_birth_sanitized).map(
        lambda time_delta: int(time_delta.days // AVARAGE_DAYS_IN_A_YEAR)
    ).rename("age")
    data.insert(0, "age", age)
    data.drop("year", axis=1, inplace=True)
    data.drop("birthdate", axis=1, inplace=True)
    return data


def get_player_position(data: pd.DataFrame) -> pd.Series:
    return pd.Series(data["positionId"])


def parse_and_replace_htwt(data):
    def parse_height(height):
        feet, inches = map(lambda s: s[:1], height.split())
        centimeters = (
            FEET_TO_CENTIMETER*float(feet) + INCHES_TO_CENTIMETER*float(inches)
        )
        return centimeters
    def parse_weight(weight):
        weight = float(weight.split()[0].split()[0])
        return POUNDS_TO_KILOGRAMS*weight
    htwt = data["htwt"].str.split(", ", expand=True)
    height = htwt.iloc[:, 0].map(parse_height)
    weight = htwt.iloc[:, 1].map(parse_weight)
    data.insert(0, "height/cm", height)
    data.insert(0, "weight/kg", weight)
    data.drop("htwt", axis=1, inplace=True)
    return data


def average_and_replace_per_minute_infos(data):
    keys = INFO_TO_AVERAGE_PER_MINUTE
    data[keys] = data[keys].div(data["minutes"], axis=0)
    data.rename(
        columns={col: col + "_per_minute" for col in keys},
        inplace=True
    )
    return data


def get_sanitized_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data = pd.DataFrame(data[~data["htwt"].isna()])
    data = data.loc[:, data.columns.isin(INFO_TO_CONSIDER)]
    data = parse_and_replace_htwt(data)
    data = parse_and_replace_salary(data)
    data = get_and_replace_age(data)
    data = average_and_replace_per_minute_infos(data)
    return data
