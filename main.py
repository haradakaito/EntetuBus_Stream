from _getbustable import GetBusTable

if __name__ == '__main__':
    # バス時刻表を取得
    getbustable = GetBusTable()
    result = getbustable._get_bustable(from_station='浜松学院大学', to_station='浜松駅')
    print(result)