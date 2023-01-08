import pandas as pd
from apriori_algo import apriori, get_rules

df = pd.read_excel(
    "Binary_dataset.xlsx", 
    usecols="D:K", index_col=0,
    skiprows=3, nrows=155
)

transactions = [
    { item for item in df if df[item][transaction] == 1 }
    for transaction in range(1, 154)
]

if __name__ == "__main__":
    result = apriori(tuple(df), transactions, 0.5)
    rules = get_rules(result, 0.75)

    for x, y, conf in rules:
        print(f"{x}\t->\t{y}\t={conf:.3f}")