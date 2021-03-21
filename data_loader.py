from pathlib import Path
import pandas as pd
import jsonlines


def jsonl_to_pd_dataframe(filepath):
    with jsonlines.open(filepath) as reader:
        data = [obj for obj in reader]
    return pd.DataFrame.from_records(data)


def get_merged_data():
    data_folder = Path("data/")

    deliveries_path = data_folder / "deliveries.jsonl"
    products_path = data_folder / "products.jsonl"
    sessions_path = data_folder / "sessions.jsonl"
    users_path = data_folder / "users.jsonl"

    deliveries_df = jsonl_to_pd_dataframe(deliveries_path)
    products_df = jsonl_to_pd_dataframe(products_path)
    sessions_df = jsonl_to_pd_dataframe(sessions_path)
    users_df = jsonl_to_pd_dataframe(users_path)

    sessions_df = pd.merge(sessions_df, users_df, how="left", on="user_id")
    sessions_df = pd.merge(sessions_df, products_df, how="left", on="product_id")
    sessions_df = pd.merge(sessions_df, deliveries_df, how="left", on="purchase_id")

    return sessions_df
