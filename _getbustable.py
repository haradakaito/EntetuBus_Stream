import requests

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GetBusTable:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--log-level=3')
        prefs = {"profile.managed_default_content_settings.images":2}
        options.headless = True
        options.add_experimental_option("prefs", prefs)
        self.chrome = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.chrome.get('https://info.entetsu.co.jp/navi/pc/annai.aspx')

    def get_bustable(self, from_station:str, to_station:str) -> list:
        # アクセスするURL
        url = self._get_bustable_url(from_station=from_station, to_station=to_station)
        result = {'取得日時':datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
        # HTTPリクエストを送信
        response = requests.get(url)
        # HTMLを解析する
        soup = BeautifulSoup(response.text, 'html.parser')
        # テーブルを取得
        table = soup.find('table')
        # ヘッダーを取得
        headers = [header.text.strip() for header in table.find_all('th')]
        # 行を取得
        rows = []
        for row in table.find_all('tr'):
            rows.append([data.text.strip() for data in row.find_all('td')])
        # データを整形
        data = [dict(zip(headers, row)) for row in rows if len(row) > 0]
        bus_state = []
        for d in data:
            del d[''], d['行き先'], d['所要時間']
            # 通過したバスは表示しない
            if d['現在地'] == '通過':
                continue
            else:
                bus_state.append(d)
        result['バス時刻表'] = bus_state
        return [result]

    # バス時刻表URLを取得する
    def _get_bustable_url(self, from_station:str, to_station:str) -> str:
        # 浜松学院大学から浜松駅まででバス停検索する
        bus_station_info = {'from': from_station, 'to': to_station}
        input_from_element = self.chrome.find_element(By.ID, 'ctl00_ContentPlaceHolder2_TBusFrom')
        input_to_element = self.chrome.find_element(By.ID, 'ctl00_ContentPlaceHolder2_TBusTo')
        input_from_element.send_keys(bus_station_info['from'])
        input_to_element.send_keys(bus_station_info['to'])
        # 検索ボタンをクリック
        search_button = self.chrome.find_element(By.ID, 'ctl00_ContentPlaceHolder2_BtnSearch')
        search_button.click()
        # 決定ボタンをクリック
        result_button = self.chrome.find_element(By.ID, 'ctl00_ContentPlaceHolder2_BtnResult')
        result_button.click()
        # バスどこをクリック
        link_element = self.chrome.find_element(By.ID, 'ctl00_ContentPlaceHolder2_LinkBusdokoFrom')
        link_element.click()
        # タブを切り替える
        self.chrome.switch_to.window(self.chrome.window_handles[1])
        # 現在のURLを取得
        current_url = self.chrome.current_url
        self.chrome.quit()
        return current_url