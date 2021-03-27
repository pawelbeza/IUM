import math
from pathlib import Path

import pandas
import pandas as pd
import jsonlines

import datetime


def jsonl_to_pd_dataframe(filepath):
    with jsonlines.open(filepath) as reader:
        data = [obj for obj in reader]
    return pd.DataFrame.from_records(data)


def get_merged_data():
    data_folder = Path("data/")

    # deliveries_path = data_folder / "deliveries.jsonl"
    products_path = data_folder / "products.jsonl"
    sessions_path = data_folder / "sessions.jsonl"
    # users_path = data_folder / "users.jsonl"

    # deliveries_df = jsonl_to_pd_dataframe(deliveries_path)
    products_df = jsonl_to_pd_dataframe(products_path)
    sessions_df = jsonl_to_pd_dataframe(sessions_path)
    # users_df = jsonl_to_pd_dataframe(users_path)

    # sessions_df = pd.merge(sessions_df, users_df, how="left", on="user_id")
    sessions_df = pd.merge(sessions_df, products_df, how="left", on="product_id")
    # sessions_df = pd.merge(sessions_df, deliveries_df, how="left", on="purchase_id")

    return sessions_df


def add_purchase_attrib(data, df_group):
    last_session_log = df_group.iloc[-1]

    is_purchased = last_session_log['event_type'] == 'BUY_PRODUCT'

    for row_index, row in df_group.iterrows():
        data.loc[row_index, 'purchase'] = is_purchased


def add_time_specific_attribs(data, df_group):
    date_format = '%Y-%m-%dT%H:%M:%S'

    first_session_log = df_group.iloc[0]

    session_date_start = datetime.datetime.strptime(first_session_log['timestamp'], date_format)
    for row_index, row in df_group.iterrows():
        session_date_end = datetime.datetime.strptime(row['timestamp'], date_format)

        data.loc[row_index, 'duration'] = (session_date_end - session_date_start).total_seconds()
        data.loc[row_index, 'weekend'] = session_date_end.weekday() >= 5
        data.loc[row_index, 'month'] = session_date_end.strftime("%B")
        data.loc[row_index, 'day'] = session_date_end.day
        data.loc[row_index, 'hour'] = session_date_end.hour


def add_event_specific_attribs(data, df_group):
    date_format = '%Y-%m-%dT%H:%M:%S'

    total_viewed_items = 0
    product_set = set()

    first_session_log = df_group.iloc[0]
    session_date_start = datetime.datetime.strptime(first_session_log['timestamp'], date_format)

    for row_index, row in df_group.iterrows():
        session_date_end = datetime.datetime.strptime(row['timestamp'], date_format)
        minutes = (session_date_end - session_date_start).total_seconds() / 60.0

        total_viewed_items += 1
        product_set.add(row.product_id)

        data.loc[row_index, 'unique_item_views'] = len(product_set)
        data.loc[row_index, 'item_views'] = total_viewed_items
        data.loc[row_index, 'click_rate'] = total_viewed_items / minutes if minutes != 0 else 0


def add_product_specific_attrib(data, df_group):
    unique_categories = set()
    for row_index, row in df_group.iterrows():
        main_category = row.category_path.split(';', 1)[0] if not pandas.isna(row.category_path) else ''
        unique_categories.add(main_category)
        data.loc[row_index, 'unique_categories'] = len(unique_categories)


def add_new_attributes(data):
    for _, df_group in data.groupby('session_id'):
        add_time_specific_attribs(data, df_group)
        add_event_specific_attribs(data, df_group)
        add_product_specific_attrib(data, df_group)
        add_purchase_attrib(data, df_group)


def get_data():
    sessions = get_merged_data()

    add_new_attributes(sessions)

    columns_to_drop = ['product_id', 'purchase_id', 'timestamp', 'timestamp', 'event_type', 'product_name',
                       'category_path', 'price']
    sessions = sessions.drop(columns_to_drop, axis=1)

    return sessions
