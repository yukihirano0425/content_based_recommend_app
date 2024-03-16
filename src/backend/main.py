import pandas as pd
import random

from data_loader.load_dataset import (
    extract_latest_month,
    merge_category_id,
    DATA_DIR,
    TRANSACTION_COLS,
    CATEGORY_COLS,
)
from features.get_frequent_category import get_frequent_category

ad_images_info = [
    {"image_path": "data/ad_image/hatomugi.png", "category": "消耗品"},
    {"image_path": "data/ad_image/hatomugi_2.png", "category": "消耗品"},
    {"image_path": "data/ad_image/chocolate.png", "category": "飲食"},
    {"image_path": "data/ad_image/application.png", "category": "ゲーム"},
    {"image_path": "data/ad_image/lunch-box.png", "category": "コンビニ"},
]

ad_image_paths = {}
for info in ad_images_info:
    if info["category"] in ad_image_paths:
        ad_image_paths[info["category"]].append(info["image_path"])
    else:
        ad_image_paths[info["category"]] = [info["image_path"]]
"""
{
    "消耗品": ["data/ad_image/hatomugi.png", "data/ad_image/hatomugi_2.png"],
    "飲食": ["data/ad_image/chocolate.png"],
    "ゲーム": ["data/ad_image/application.png"],
    "コンビニ": ["data/ad_image/lunch-box.png"],
}
"""


def assign_ad_image_path(frequent_category: str):
    if frequent_category in ad_image_paths:
        return random.choice(ad_image_paths[frequent_category])
    else:
        all_images = [path for paths in ad_image_paths.values() for path in paths]
        return random.choice(all_images)


def main():
    transaction_df = extract_latest_month(
        pd.read_csv(DATA_DIR + "取引明細_transactions.csv")
    )[TRANSACTION_COLS]
    category_df = pd.read_csv(DATA_DIR + "カテゴリマスタ_categories.csv")[CATEGORY_COLS]
    spend_df = transaction_df[transaction_df["amount"] < 0]
    merged_df = merge_category_id(spend_df, category_df, "category_id", "id")

    frequent_category_df = get_frequent_category(merged_df, "account_id", "name_ja")

    frequent_category_df["ad_image_path"] = frequent_category_df["name_ja"].apply(
        assign_ad_image_path
    )
    print(frequent_category_df[["account_id", "name_ja", "ad_image_path"]])

    return frequent_category_df


if __name__ == "__main__":
    main()
