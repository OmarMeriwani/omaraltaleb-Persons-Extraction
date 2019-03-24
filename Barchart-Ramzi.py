import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt;

def plot_bargraph_with_groupings(df, groupby, colourby, title, xlabel, ylabel):
    """
    Plots a dataframe showing the frequency of datapoints grouped by one column and coloured by another.
    df : dataframe
    groupby: the column to groupby
    colourby: the column to color by
    title: the graph title
    xlabel: the x label,
    ylabel: the y label
    """

    import matplotlib.patches as mpatches

    # Makes a mapping from the unique colourby column items to a random color.
    ind_col_map = {x:y for x, y in zip(df[colourby].unique(),
                               [plt.cm.Paired(np.arange(len(df[colourby].unique())))][0])}


    # Find when the indicies of the soon to be bar graphs colors.
    unique_comb = df[[groupby, colourby]].drop_duplicates()
    name_ind_map = {x:y for x, y in zip(unique_comb[groupby], unique_comb[colourby])}
    c = df[groupby].value_counts().index.map(lambda x: ind_col_map[name_ind_map[x]])

    # Makes the bargraph.
    ax = df[groupby].value_counts().plot(kind='bar',
                                         figsize=(2250,2625),
                                         title=title,
                                         color=[c.values])
    # Makes a legend using the ind_col_map
    legend_list = []
    for key in ind_col_map.keys():
        legend_list.append(mpatches.Patch(color=ind_col_map[key], label=key))

    # display the graph.
    plt.legend(handles=legend_list)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


plt.rcdefaults()
plt.rcParams["font.family"] = "Times"

df = pd.read_csv('Figure-1.csv')
df = df['Type'].value_counts()

df.plot(kind='bar',
        fontsize=12, zorder=2)
plt.rcParams['font.family'] = "sans-serif"
plt.xticks(rotation='horizontal')
plt.xlabel('IBS subtypes')
plt.ylabel('Number of cases')
plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
plt.show()
