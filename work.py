import pandas as pd
import numpy as np

np.random.seed(42)  # For reproducibility

n = 32

data = {
    "uniqueID": range(1, n + 1),
    "remQTime": np.random.randint(1, 12, n),
    "qty": np.random.randint(1, 20, n),
    "recipeID": np.random.randint(1, 7, n),
    "waitingTime": np.random.randint(1, 50, n)
}

df = pd.DataFrame(data)
df_list = [df[df['remQTime'] < 6], df[df['remQTime'] >= 6]]
for i, tmp_df in enumerate(df_list):
    tmp_df_lst = []
    rest_df = pd.DataFrame(columns=df.columns)
    for recipe, group in tmp_df.groupby('recipeID', sort=False):
        if len(group) >= 2:
            tmp_df_lst.append(group)
        else:
            rest_df = pd.concat([rest_df, group], ignore_index=True)

    # If there are remaining items that did not fit into any group, add them as a single group
    if not rest_df.empty:
        tmp_df_lst.append(rest_df)
    df_list[i] = tmp_df_lst

result_df = pd.DataFrame(columns=df.columns)

for j, qtime_grp in enumerate(df_list):
    for i, tmp_df in enumerate(qtime_grp):
        tmp_pairs = []
        remaining = pd.DataFrame()
        low_qty = tmp_df[tmp_df['qty'] < 6]
        high_qty = tmp_df[tmp_df['qty'] > 13]
        rest = tmp_df[(tmp_df['qty'] <= 13) & (tmp_df['qty'] >= 6)]

        min_idx = min(len(low_qty), len(high_qty))

        for i in range(min_idx):
            tmp_pairs.append((low_qty.iloc[i], high_qty.iloc[i]))
        
        if len(low_qty) > len(high_qty):
            remaining = low_qty.iloc[min_idx:]
        elif len(low_qty) < len(high_qty):
            remaining = high_qty.iloc[min_idx:]

        remaining = pd.concat([rest, remaining], ignore_index=True)
        tmp_pairs = sorted(tmp_pairs, key=lambda x: x[0]['waitingTime'], reverse=True)
        
        for pair in tmp_pairs:
            if not pair[0].empty or not pair[1].empty:
                result_df = pd.concat([result_df, pd.DataFrame([pair[0]])], ignore_index=True)
                result_df = pd.concat([result_df, pd.DataFrame([pair[1]])], ignore_index=True)

        if not remaining.empty:
            remaining = remaining.sort_values(by='waitingTime', ascending=False)
            result_df = pd.concat([result_df, remaining], ignore_index=True)

print(result_df)
