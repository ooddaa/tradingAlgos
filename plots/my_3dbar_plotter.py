def df_combiner(dfs):
    for i in range(len(dfs)):
        if i < len(dfs)-1:
            if i == 0:
                x = dfs[i]
            x = x.combine_first(dfs[i+1])
    return x

def df_to_3Dbars(misdf):
    # MIS DataFrame is 
    # rows == days of observations
    # cols = expirations
    # values = MIS
    arr = []

    for idx in misdf.index:
        for col in misdf.columns:
            bar = [col, idx, misdf.loc[idx, col]]
            arr.append(bar)
    
    x = [] 
    y = [] 
    z = []

    for bar in arr:
        col, idx, strike = bar
        x.append(col)
        y.append(idx)
        z.append(strike)
        
    return x, y, z

def plotter(x, y, z, width=1, depth=1, ax=False, figsize=False, labels=['x', 'y', 'z']):
    
    # defaults
    figsize = (10,10) if figsize is False else figsize
    
    if ax is False:
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')
        
    bottom = np.zeros_like(z)
    hight = z
    
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    out = ax.bar3d(x, y, bottom, width, depth, hight)
    return out

def my_3dbar_plotter(misdf, **kwargs):
    x, y, z = df_to_3Dbars(misdf)
    return plotter(x, y, z, **kwargs)