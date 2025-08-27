# pyright: basic
from pathlib import Path

import get_data as gd

def get_correlation(relevant_information):
    return relevant_information.loc[
        :, ~relevant_information.columns.isin(("playerId", "positionId"))
    ].corr()


if __name__ == "__main__":
    data = gd.get_sanitized_data()
    print("Number of players: ", gd.number_of_players(data))
    correlation = data.loc[:, ~data.columns.isin(gd.NON_METRIC_INFO)].corr()
    print(correlation["height/cm"])
    # for position, position_group in relevant_information.groupby("positionId"):
    #     print(position_group, end="\n\n")
    #     print(get_correlation(position_group), end="\n\n")
    #
    # for player_age, age_group in relevant_information.groupby("age"):
    #     print(age_group, end="\n\n")
    #     print(get_correlation(age_group), end="\n\n")
