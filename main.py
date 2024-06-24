from fastapi import FastAPI
from _getbustable import GetBusTable

app = FastAPI()
getbustable = GetBusTable()

@app.get("/")
# バス時刻表を取得
def read_bustable(from_station:str='浜松学院大学', to_station:str='浜松駅'):
    result = getbustable._get_bustable(from_station, to_station)
    return result