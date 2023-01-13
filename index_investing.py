import tools as tl
import investor

spy_df = tl.get_spy_dataframe()

print(spy_df)

# Necessary pct. changes per day
# columns: 1: pct. change 2. close/open price (depends on type pct. change)
change_open_to_close_df, change_open_to_low_df, \
    change_prev_close_to_close_df, change_prev_close_to_low_df = tl.create_dfs(spy_df)

print(change_open_to_close_df)

last_price = spy_df['Close'][spy_df.index[-1]]
print(last_price)

test = investor.Investor(change_open_to_close_df, 500, '1', 0, 1, 1, 1)
test.calculate_investments()
test.print_investment_stats(last_price)

test2 = investor.Investor(change_open_to_close_df, 100, '1', 0, 1, 0, 1)
test2.calculate_investments()
test2.print_investment_stats(last_price)

test3 = investor.Investor(change_open_to_low_df, 100, '>', -3, 1, 1, 1)
test3.calculate_investments()
test3.print_investment_stats(last_price)

test4 = investor.Investor(change_prev_close_to_low_df, 100, '<', -2, 1, 2, 1)
test4.calculate_investments()
test4.print_investment_stats(last_price)

