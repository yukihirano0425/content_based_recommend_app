import pandas as pd

DATA_DIR = "data/"
TRANSACTION_COLS = ["account_id", "category_id", "date", "amount", "balance_as_of"]
CATEGORY_COLS = ["id", "name_ja", "category_type"]


def extract_latest_month(df: pd.DataFrame):
    df["yyyymm"] = df["date"].str[:7].str.replace("-", "")
    df["date"] = df["date"].str[:10]
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    return df


def merge_category_id(
    spend_df: pd.DataFrame, category_df: pd.DataFrame, left_col: str, right_col: str
):
    return pd.merge(
        spend_df, category_df, left_on=left_col, right_on=right_col, how="inner"
    )


def main(
    file_path: str,
    category_df_path: str,
    category_col_for_transaction_df: str,
    category_col_for_category_df: str,
):
    transaction_df = extract_latest_month(pd.read_csv(DATA_DIR + file_path))[
        TRANSACTION_COLS
    ]
    spend_df = transaction_df[transaction_df["amount"] < 0]
    return merge_category_id(
        spend_df,
        pd.read_csv(DATA_DIR + category_df_path)[CATEGORY_COLS],
        category_col_for_transaction_df,
        category_col_for_category_df,
    )
