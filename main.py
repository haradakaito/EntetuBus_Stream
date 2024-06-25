import uvicorn

from fastapi import FastAPI
from _getbustable import GetBusTable
from _getbusstop import GetBusStop
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/latest")
# バス時刻表を取得
def read_bustable(from_station:str, to_station:str):
    try:
        getbustable = GetBusTable()
        result = getbustable.get_bustable(from_station=from_station, to_station=to_station)
        return result
    except:
        return None

@app.get("/busstop")
# バス停
def read_busstop(erea:str):
    try:
        getbusstop = GetBusStop()
        result = [getbusstop.get_busstop(erea=erea)]
        return result
    except:
        return None

if __name__ == "__main__":
    uvicorn.run(feisty-courage.app, host="0.0.0.0", port=8000, reload=True)