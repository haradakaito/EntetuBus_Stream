from fastapi import FastAPI
from _getbustable import GetBusTable
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
# バス時刻表を取得
def read_bustable(from_station:str, to_station:str):
    try:
        getbustable = GetBusTable()
        result = getbustable._get_bustable(from_station, to_station)
        return result
    except:
        return None