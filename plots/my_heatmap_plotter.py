

def my_heatmap_plotter(x, y, z, zlabel='Open Interest',
                       ax=False,
                       figsize=False,
                       title='Most Interesting Contract'
                       ):
    # defaults
    figsize = (10, 10) if figsize is False else figsize

    if ax is False:
        fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(z)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(zlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(x)))
    ax.set_yticks(np.arange(len(y)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(x, rotation=45, ha="right",
                       rotation_mode="anchor")
    ax.set_yticklabels(y)

    ax.set_title(title)
    # fig.tight_layout()
