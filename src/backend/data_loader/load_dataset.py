import pandas as pd

DATA_DIR = "data/"


def read_spend_dataset(data_dir: str, file_name: str):
    df = pd.read_csv(f"{data_dir}{file_name}")
    return df[df["amount"] < 0]


def extract_latest_month(df: pd.DataFrame):
    df["yyyymm"] = df["date"].str[:7].str.replace("-", "")
    df["date"] = df["date"].str[:10]
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    return df


df = read_spend_dataset(DATA_DIR, "取引明細_transactions.csv")
print(extract_latest_month(df))
