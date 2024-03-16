import pandas as pd

# TODO: 「カード返済」「ATM引き出し」「振替」「振込手数料」「手数料」など特定カテゴリを排除する
# TODO: 消費カテゴリごとの重み付けを行う
# TODO: カテゴリを算出する月を限定する？（最新月など）
# TODO: カテゴリがないuserに対しては、どのようにカテゴリ付与するのか考える


def get_frequent_category(
    df: pd.DataFrame, account_id_col: str, category_col: str
) -> pd.DataFrame:
    grouped = (
        df.groupby([account_id_col, category_col]).size().reset_index(name="counts")
    )
    return grouped.sort_values("counts", ascending=False).drop_duplicates(
        account_id_col
    )
