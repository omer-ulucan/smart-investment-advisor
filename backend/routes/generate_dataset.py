from fastapi import APIRouter, Query
import yfinance as yf
import pandas as pd
from backend.utils.supabase_integration import insert_data_to_supabase
from backend.utils.data_preprocessing import save_dataset_csv, save_raw_data
from backend.config import TRAINING_DATA_CSV

router = APIRouter()

def fetch_historical_data(stock_symbol: str) -> pd.DataFrame:
    ticker = yf.Ticker(stock_symbol)
    data = ticker.history(period="10y")
    data.reset_index(inplace=True)
    data['stock_symbol'] = stock_symbol

    data.rename(columns={
    'Date': 'date',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Volume': 'volume',
    'Dividends': 'dividends',
    'Stock Splits': 'stock_splits'
    }, inplace=True)


    data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d")
    return data

@router.get("/generate-dataset-multiple")
async def generate_dataset_multiple(
    stocks: str = Query(..., description="Virgülle ayrılmış hisse sembolleri, örn: AAPL,MSFT,GOOG")
):
    try:
        symbols = [sym.strip() for sym in stocks.split(",")]
        combined_df = pd.DataFrame()

        for symbol in symbols:
            df = fetch_historical_data(symbol)
            save_raw_data(df, "data/raw_data/historical", f"{symbol}_historical.csv")
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        combined_df = combined_df.drop_duplicates(subset=["date", "stock_symbol"]).reset_index(drop=True)
        save_dataset_csv(combined_df, TRAINING_DATA_CSV)
        response = insert_data_to_supabase(combined_df)
        
        return {
            "message": f"{', '.join(symbols)} için birleşik dataset oluşturuldu.",
            "supabase_response": response.data
        }
    except Exception as e:
        return {"error": str(e)}
