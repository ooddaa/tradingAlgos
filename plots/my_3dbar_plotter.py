def df_to_3Dbars(misdf):
    # MIS DataFrame is
    # rows == days of observations
    # cols = expirations
    # values = MIS
    arr = []

    for idx in misdf.index:
        for col in misdf.columns:
            bar = [idx, col, misdf.loc[idx, col]]
            arr.append(bar)

    x = []
    y = []
    z = []

    for bar in arr:
        idx, col, strike = bar
        x.append(idx)
        y.append(col)
        z.append(strike)

    return x, y, z


def plotter(x, y, z,
            width=1,
            depth=1,
            ax=False,
            figsize=False,
            labels=['x', 'y', 'z'],
            xticks=False,
            xticklabels=False
            ):

    # defaults
    figsize = (10, 10) if figsize is False else figsize

    if ax is False:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')

    bottom = np.zeros_like(z)
    hight = z

    # ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])

    # set xticks and xticks labels
    # https://matplotlib.org/3.1.3/api/_as_gen/matplotlib.axes.Axes.set_xticks.html
    # https://stackoverflow.com/questions/14852821/aligning-rotated-xticklabels-with-their-respective-xticks
    if xticks is not False:
        print('len xticks:', len(xticks))
        ax.set_xticks(xticks,
                      minor=False
                      )
    else:
        ax.set_xticks(range(0, len(x)))  # or default

    if xticklabels is not False:
        # https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.axes.Axes.set_xticklabels.html
        # print('xticklabels:', xticklabels)
        ax.set_xticklabels(xticklabels,
                           rotation=45,
                           ha='right'
                           )

    out = ax.bar3d(x, y, bottom, width, depth, hight)
    return out


def my_3dbar_plotter(misdf, **kwargs):
    x, y, z = df_to_3Dbars(misdf.loc[:, misdf.columns != 'index'])
    return plotter(x, y, z,
                   xticks=range(0, len(misdf['index'])),
                   xticklabels=misdf['index'],
                   **kwargs
                   )
