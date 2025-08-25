# pyright: basic
import datetime
from pathlib import Path

import pandas as pd

AVARAGE_DAYS_IN_A_YEAR = 365.2425
FEET_TO_CENTIMETER = 30.48
INCHES_TO_CENTIMETER = 2.54
POUNDS_TO_KILOGRAMS = 0.4535924

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


def unique_ages(data):
    return get_ages(data).unique()


def split_height_and_weight(data):
    def get_height(htwt):
        height = htwt.split(",")[0].strip()
        feet, inches = map(lambda s: s[:1], height.split())
        centimeters = FEET_TO_CENTIMETER*float(feet) + INCHES_TO_CENTIMETER*float(inches)
        return centimeters
    def get_weight(htwt):
        weight = float(htwt.split(",")[1].strip().split()[0].split()[0])
        return POUNDS_TO_KILOGRAMS*weight
    height = data["htwt"].map(get_height).rename("height")
    weight = data["htwt"].map(get_weight).rename("weight")
    return (height, weight)


if __name__ == "__main__":
    data = pd.read_csv(Path("nba_stats.csv"))
    data = data[~data["htwt"].isna()]
    # data = data[data["htwt"].isna()]
    # relevant_information = pd.concat(
    #     [data["playerId"].to_frame().T, get_ages(data).to_frame().T]
    # ).T
    # print(relevant_information)
    # print(unique_ids(data))
    # print(number_of_players(data))
    # print(get_ages(data))
    # x = unique_ages(data)
    # print(x)
    # x.sort()
    # print(x)
    print(split_height_and_weight(data))
