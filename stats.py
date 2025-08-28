# pyright: basic
import pandas as pd
import numpy as np

NON_METRIC_INFO = [
    "year",
    "playerId",
    "positionId",
    "birthdate",
    "htwt",
]

def get_correlation_by_position(data: pd.DataFrame):
    correlations = []
    for position, position_group in data.groupby("positionId"):
        correlations.append(get_height_correlation(position_group))
        print(f"\nPlayer position: {position}")
        print(correlations[-1])

def get_correlation_by_age(data: pd.DataFrame):
    correlations = []
    for player_age, age_group in data.groupby("age"):
        correlations.append(get_height_correlation(age_group))
        print(f"Player age: {player_age}")
        print(correlations[-1], end="\n\n")

def get_correlation(data: pd.DataFrame):
    correlation = data.loc[:, ~data.columns.isin(NON_METRIC_INFO)].corr()
    return correlation


def get_height_correlation(data: pd.DataFrame):
    correlation = data.loc[:, ~data.columns.isin(NON_METRIC_INFO)].corr()
    return correlation["height/cm"].sort_values(ascending=False, key=np.abs)


def number_of_players(data: pd.DataFrame):
    players_ids = data["playerId"].unique()
    return players_ids.size
