import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class GetBusStop:

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
        self.chrome.get('https://www.navitime.co.jp/bus/diagram/busstop/22138/00001037/?name=') # 静岡県 浜松市中央区 全域
        print('OK')

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