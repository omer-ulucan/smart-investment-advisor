import pandas as pd
from supabase import create_client, Client
from backend.config import SUPABASE_URL, SUPABASE_API_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def insert_data_to_supabase(df: pd.DataFrame, table_name: str = "historical_stock_data"):
    records = df.to_dict(orient="records")
    response = supabase.table(table_name).insert(records).execute()
    return response
