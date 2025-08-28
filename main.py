# pyright: basic
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import get_data as gd
import stats as st
import graphs as gp

if __name__ == "__main__":
    data = gd.get_sanitized_data()
    print(data.describe())
    print(pd.Series(data["height/cm"]).sort_values(ascending=True))
    print("Number of players: ", st.number_of_players(data))
    correlation_matrix = st.get_height_correlation(data)
    print(correlation_matrix)
    print(st.get_correlation_by_position(data))
    heights = data["height/cm"].to_numpy()
    heights.sort()
    print(heights)
    gp.show_correlation_color_map(data, save=True)
    # print(st.get_correlation_by_age(data))
