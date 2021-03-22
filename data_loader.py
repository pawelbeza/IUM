from pathlib import Path
import pandas as pd
import jsonlines

import datetime


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


def add_purchase_attrib(data):
    for group_name, df_group in data.groupby('session_id'):
        last_session_log = df_group.iloc[-1]

        is_purchased = last_session_log['event_type'] == 'BUY_PRODUCT'

        for row_index, row in df_group.iterrows():
            data.loc[row_index, 'purchase'] = is_purchased


def add_session_duration_attrib(data):
    date_format = '%Y-%m-%dT%H:%M:%S'
    for group_name, df_group in data.groupby('session_id'):
        last_session_log = df_group.iloc[0]

        session_date_start = datetime.datetime.strptime(last_session_log['timestamp'], date_format)
        for row_index, row in df_group.iterrows():
            session_date_end = datetime.datetime.strptime(row['timestamp'], date_format)
            data.loc[row_index, 'duration'] = (session_date_end - session_date_start).total_seconds()


def add_new_attributes(data):
    add_session_duration_attrib(data)
    add_purchase_attrib(data)


def get_data():
    sessions = get_merged_data()

    add_new_attributes(sessions)

    columns_to_drop = ['user_id', 'user_id', 'product_id', 'purchase_id', 'timestamp_event', 'purchase_timestamp',
                       'street']
    sessions = sessions.drop(columns_to_drop, axis=1)

    return sessions
