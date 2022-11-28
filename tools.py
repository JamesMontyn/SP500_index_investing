import yfinance as yf
import pandas as pd

def get_spy_dataframe():
    """Gets the SPY dataframe from yahoofinance and returns it"""
    spy_df = yf.download('SPY',
                         period='max',
                         interval='1d',
                         rounding=False,
                         progress=False)

    if spy_df.empty:
        print('DataFrame is Empy, did not successfully download SPY data!')

    return spy_df


def create_dfs(spy_df):
    """Fills the dfs with the different pct. changes per date

    Parameters
    ----------
    spy_df: pandas data frame
        SPY dataframe

    Returns
    -------
    change_open_to_close: pandas data frame
        empty df to fill with pct. change between Open and Close

    change_open_to_low: pandas data frame
        empty df to fill with pct. change between Open and Low

    change_prev_close_to_close: pandas data frame
        empty df to fill with pct. change between Close of previous day and Close

    change_prev_close_to_low: pandas data frame
        empty df to fill with pct. change between Close of previous day and Low
    """
    change_open_to_close = []  # Pct change between Open and Close
    change_open_to_low = []  # Pct change between Open and Low
    change_prev_close_to_close = []  # Pct change between Close of previous day and Close
    change_prev_close_to_low = []  # Pct change between Close of previous day and Low

    prev_close = spy_df['Close'][0]

    for date in spy_df.index:
        change_open_to_close.append(((spy_df['Close'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
        change_open_to_low.append(((spy_df['Low'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
        change_prev_close_to_close.append(((spy_df['Close'][date] - prev_close) / prev_close) * 100)
        change_prev_close_to_low.append(((spy_df['Low'][date] - prev_close) / prev_close) * 100)
        prev_close = spy_df['Close'][date]

    change_open_to_close_df = pd.DataFrame(index=spy_df.index,
                                           columns=['Pct. Open to Close'],
                                           data=change_open_to_close)
    change_open_to_low_df = pd.DataFrame(index=spy_df.index,
                                         columns=['Pct. Open to Low'],
                                         data=change_open_to_low)
    change_prev_close_to_close_df = pd.DataFrame(index=spy_df.index,
                                                 columns=['Pct. Prev. Close to Close'],
                                                 data=change_prev_close_to_close)
    change_prev_close_to_low_df = pd.DataFrame(index=spy_df.index,
                                               columns=['Pct. Prev. Close to Low'],
                                               data=change_prev_close_to_low)

    return change_open_to_close_df, change_open_to_low_df, change_prev_close_to_close_df, change_prev_close_to_low_df
