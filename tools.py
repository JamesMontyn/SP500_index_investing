import yfinance as yf


def get_spy_dataframe():
    spy_df = yf.download('SPY',
                         period='max',
                         interval='1d',
                         rounding=False,
                         progress=False)

    if spy_df.empty:
        print('DataFrame is Empy, did not successfully download SPY data!')

    return spy_df


def fill_lists(spy_df, change_open_to_close, change_open_to_low,
               change_prev_close_to_close, change_prev_close_to_low):
    prev_close = spy_df['Close'][0]

    for date in spy_df.index:
        change_open_to_close.append(((spy_df['Close'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
        change_open_to_low.append(((spy_df['Low'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
        change_prev_close_to_close.append(((spy_df['Close'][date] - prev_close) / prev_close) * 100)
        change_prev_close_to_low.append(((spy_df['Low'][date] - prev_close) / prev_close) * 100)
        prev_close = spy_df['Close'][date]
