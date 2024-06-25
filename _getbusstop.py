import requests
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class GetBusStop:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        options.add_argument('--log-level=3')  # INFO以上のログのみ表示
        os.chmod('chromedriver.exe', 755)
        self.chrome_service = webdriver.ChromeService(executable_path='chromedriver.exe')
        self.chrome = webdriver.Chrome(service=self.chrome_service, options=options)
        self.chrome.get('https://www.navitime.co.jp/bus/diagram/busstop/22138/00001037/?name=') # 静岡県 浜松市中央区 全域

    # 任意のエリアのバス停の情報を取得する
    def get_busstop(self, erea:str) -> list:
        result = {}
        # アクセスするURLを取得
        url = self._get_busstop_url(erea=erea)
        # HTTPリクエストを送信
        response = requests.get(url)
        # HTMLを解析する
        soup = BeautifulSoup(response.text, 'html.parser')
        # バス停の情報を取得
        busstops = []
        for li in soup.select('ul.node-list li'):
            busstop_name = li.find('a').text.strip()
            busstops.append(busstop_name)
        result['バス停'] = busstops
        return result

    # バス停のURLを取得する
    def _get_busstop_url(self, erea:str) -> str:
        # 地域を入力
        select_element = self.chrome.find_element(By.ID, 'address-level-3')
        select_element.send_keys(erea)
        # 絞り込み検索ボタンをクリック
        search_button = self.chrome.find_element(By.ID, 'submit_busstop_search')
        search_button.click()
        # URLを取得
        current_url = self.chrome.current_url
        self.chrome.quit()
        return current_url