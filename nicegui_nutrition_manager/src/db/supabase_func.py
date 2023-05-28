from supabase import create_client, Client
from dotenv import load_dotenv
import os
from dataclasses import asdict, dataclass

load_dotenv()


def supabase_client() -> Client:
    # client initialization
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_SECRET")
    supabase: Client = create_client(url, key)
    return supabase


def loading_collection(client, collection_name: str):
    result = client.collection(collection_name).get_full_list()
    record_lst = [record for record in result]
    return record_lst


def insert_as_dict_supabase(table_name: str, data: dataclass) -> dict:
    supabase = supabase_client()
    dct = asdict(data)
    # print(dct)
    send_data = supabase.table(table_name).insert(dct).execute()
    assert len(send_data.data) > 0
    return asdict(data)


def select_all(table_name: str, column_name: str):
    supabase = supabase_client()
    data = supabase.table(table_name).select(column_name).execute()
    assert len(data.data) > 0
    return data.data


def select_filtered(table_name: str, cols: str, filter_col: str, filter_value: str):
    supabase = supabase_client()
    data = supabase.table(table_name).select(cols).eq(filter_col, filter_value).execute()
    assert len(data.data) > 0
    return data.data




