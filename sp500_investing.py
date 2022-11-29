import tools as tl
import investor

spy_df = tl.get_spy_dataframe()

print(spy_df)

# Necessary pct. changes per day
# columns: 1: pct. change 2. close/open price (depends on type pct. change)
change_open_to_close_df, change_open_to_low_df, \
    change_prev_close_to_close_df, change_prev_close_to_low_df = tl.create_dfs(spy_df)

print(change_open_to_close_df)

test = investor.Investor(change_open_to_close_df, 100, '1', 0, 1, 1, 1)
test.calculate_investments()

"""
# Results dataframe
results_df = pd.DataFrame(index=spy_df.index)

print(results_df)

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
