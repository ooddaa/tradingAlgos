import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta

# parse contractSymbol date
def parse_contractSymbol(cs, rdate=False, asdict=False):
    #     cs = 'PLTR210108C00025000'
    ticker = cs [:-15]
    year = cs[-15:-13]
    month = cs[-13:-11]
    day = cs[-11:-9]
    instr_type = cs[-9]
    strike = float(cs[-8:])/1000
    
    if rdate == True:
        return date(2000+int(year), int(month), int(day))
    
    if asdict == True:
        return {
            'ticker': ticker,
            'year': year,
            'month': month,
            'day': day,
            'instr_type': instr_type,
            'strike': strike,
        }
    return (ticker, year, month, day, instr_type, strike)

# parse_contractSymbol('PLTR210108C00025000') # ('PLTR', '21', '01', '08', 'C', 25.0)
# parse_contractSymbol('PLTR210108C00025000', rdate=True) # 

# pick one the most interesting contract symbol
def max_interest_by(df, col='openInterest'):
    return df.loc[df.sort_values(by=[col], ascending=False)[col].idxmax()] # Series


# ('2021-01-15', 30.0, 80195)

def add_z_score(df, column='openInterest'):
    """
    Calculates z-score based on values of the given column. 
    Appends a column with stored results.
    """
    new_df = df.copy()
    new_df[column+'Z'] = (df[column] - df[column].mean())/df[column].std()
    return new_df


def filter_by_z_score(df, column='openInterest', mean=True, let=.5):
    """
    Filters df by its z-score. 
    mean - if True, takes all values higher than mean z-score
    let - larger or equal than value
    """
    if mean:
        return df.loc[df[column+'Z'] > df[column+'Z'].describe()['mean']]
    
    return df.loc[df[column+'Z'] >= let]


def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    return True

def filter_by_date(df, date, column='exp'):
    """
    Second argument must be a datetime.date object
    """
    #     if not datetime_valid(str(date)):
    #         raise Exception(f"Second positional argument must be valid iso format date - yyyy-mm-dd. Received {date}")
    #     if type(date) is not 'datetime.date':
    #         raise Exception(f"Second positional argument must be datetime.date object. Received {type(date)}")
    return df[df[column] == date]

    
# filter_by_date(calls, exps[4])

# filter_by_z_score(add_z_score(filter_by_date(calls, exps[0]), column='volume'), column='volume')

def calculate_horizon_date(time_horizon):
    """
    Maps time_horizon = ['next', '1mo', '3mo', '6mo', '1y', '2y', 'max'] to datetime.date object
    """
    today = date.today()
    if time_horizon == '1w':
        return today + timedelta(7)
    if time_horizon == '2w':
        return today + timedelta(7*2)
    if time_horizon == '3w':
        return today + timedelta(7*3)
    if time_horizon == '1mo':
        return today + timedelta(31*1)
    if time_horizon == '3mo':
        return today + timedelta(31*3)
    if time_horizon == '6mo':
        return today + timedelta(31*6)
    if time_horizon == '1y':
        return today + timedelta(365)
    if time_horizon == '2y':
        return today + timedelta(365*2)
    if time_horizon == 'max':
        return today + timedelta(365*100)
    raise Exception("time_horizon must be ['1w', '2w', '3w', '1mo', '3mo', '6mo', '1y', '2y', 'max']")
    
def interesting_options(op_chain, column='openInterest', time_horizon='max', filter_by_expiration=True, z_score_mean=True, z_score_let=False):
    """
    Takes a full option chain and filters based on z-score. 
    
    time_horizon = ['1w', '2w', '3w', '1mo', '3mo', '6mo', '1y', '2y', 'max']
    """
    
    df = op_chain.copy()
    
    # add expiration column
    df['exp'] = df['contractSymbol'].apply(lambda cs: parse_contractSymbol(cs, rdate=True))

    # filter by time_horizon
    horizon_date = calculate_horizon_date(time_horizon)
    df = df[df['exp'] <= horizon_date]
    
    # get unique expirations
    exps = df['exp'].unique() # (13,)
    
    # add stike column
    df['strike'] = df['contractSymbol'].apply(lambda cs: parse_contractSymbol(cs, asdict=True)['strike'])
    
    # set convinient dates and strikes for plot
    # df['date_strike'] = df['exp'].apply(lambda d: d.strftime('20%y-%m-%d'))

    def make_date_strike(cs):
        (ticker, year, month, day, instr_type, strike) = parse_contractSymbol(cs)
        return f"20{year}-{month}-{day} {strike}"
    
    df['date_strike'] = df['contractSymbol'].apply(lambda d: make_date_strike(d))
    
    # adding z-score
    new_df = pd.DataFrame([], columns=df.columns)
    for exp in exps:
        by_date = filter_by_date(df, exp) # filter by expiration date
        with_z = add_z_score(by_date, column=column)
        filtered_by_z = filter_by_z_score(with_z, 
                                          column=column, 
                                          mean=z_score_mean, 
                                          let=z_score_let)
        new_df = pd.concat([new_df, filtered_by_z], axis=0, ignore_index=True)
        
    return new_df