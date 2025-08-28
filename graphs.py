# pyright: basic
import pandas as pd
from matplotlib import pyplot as plt

import stats as st

def show_correlation_color_map(data: pd.DataFrame, save=False):
    corr_matrix = st.get_correlation(data)
    columns = list(corr_matrix.columns)
    cm = plt.get_cmap('inferno') # jet, viridis, inferno, plasma

    plt.matshow(corr_matrix, cmap = cm)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('r')

    ax = plt.gca()
    ax.set_xticks(range(len(columns)))
    ax.set_yticks(range(len(columns)))
    ax.set_xticklabels(columns)
    ax.set_yticklabels(columns)

    plt.setp(
        ax.get_xticklabels(),
        rotation = 45,
        ha = 'left',
        rotation_mode='anchor',
    )

    if save:
        plt.savefig("corr_matrix.png")
