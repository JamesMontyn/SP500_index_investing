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
test.print_data_frame(False)
test.data_frame_to_csv("testdata.csv")
