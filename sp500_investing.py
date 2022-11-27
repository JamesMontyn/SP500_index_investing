import pandas as pd
import tools as tl


spy_df = tl.get_spy_dataframe()

print(spy_df)

# Necessary pct. changes per day
change_open_to_close = []  # Pct change between Open and Close
change_open_to_low = []  # Pct change between Open and Low
change_prev_close_to_close = []  # Pct change between Close of previous day and Close
change_prev_close_to_low = []  # Pct change between Close of previous day and Low

tl.fill_lists(spy_df, change_open_to_close, change_prev_close_to_low,
              change_prev_close_to_close, change_prev_close_to_low)

# Results dataframe
results_df = pd.DataFrame(index=spy_df.index)

print(results_df)

"""
results_df['Pct. Open to Close'] = change_open_to_close
results_df['Pct. Open to Low'] = change_open_to_low
results_df['Pct. Prev. Close to Close'] = change_prevclose_to_close
results_df['Pct. Prev. Close to Low'] = change_prevclose_to_low

results_df['Avg. price (monthly & first day)'] = avgprice_fd
results_df['Shares (monthly & first day)'] = shares_fd

results_df['Avg. price (monthly & last day)'] = avgprice_ld
results_df['Shares (monthly & last day)'] = shares_ld

results_df['Avg. price (monthly & 2pct.)'] = avgprice_oc
results_df['Shares (monthly & 2pct.)'] = shares_oc
"""
