def concat_dfs(dfs, byindex=False, keycol='contractSymbol', valcol='openInterest', colnamepfx='day'):
    """
    Creates a 2D df where:
        1. columns correspond to observation days (for x axis).
        2. rows correspond to expirations/contract symbols (for y axis).
        3. values correspond to column data (for z axis/color)
    """
    def slice_dfs(dfs, keycol, valcol):
        out = []
        for i, df in enumerate(dfs):
            new_df = pd.DataFrame(df[valcol].values,
                                  # human readable format
                                  columns=[f'{colnamepfx}{i}'],
                                  index=df.index if byindex is True else df[keycol])  # what's our index
            out.append(new_df)
        return out

    sliced = slice_dfs(dfs, keycol, valcol)
    out_df = pd.concat(sliced, axis=1)
    out_df.fillna(0, inplace=True)
    return out_df
