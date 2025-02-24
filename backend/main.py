from fastapi import FastAPI
from backend.routes import generate_dataset

app = FastAPI()

app.include_router(generate_dataset.router)

@app.get("/")
def root():
    return {
        "message": "Birleşik dataset oluşturma API'sine hoşgeldiniz. Örneğin, /generate-dataset-multiple?stocks=AAPL,MSFT,GOOG endpoint'ini deneyin."
    }
