import pandas as pd
from apriori_algo import apriori

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
    print(*result, sep="\n")