from fastapi import FastAPI
from _getbustime import GetBusTime
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

getbustime = GetBusTime()
getbusstop = GetBusStop()

# ヘルスチェック
@app.get("/")
def read_root():
    return {"Message": "Hello Entetsu Bus Stream API!"}

# バス時刻表を取得
@app.get("/bustime")
def read_bustable(bus_from:str, bus_to:str) -> list:
    try:
        result = getbustime.get_bustime(bus_from=bus_from, bus_to=bus_to)
        return result
    except Exception as e:
        return({"error": str(e)})

# バス停一覧を取得
@app.get("/busstop")
def read_busstop(erea:str):
    try:
        result = getbusstop.get_busstop(erea=erea)
        return result
    except Exception as e:
        return({"error": str(e)})