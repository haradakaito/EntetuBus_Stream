# import pyvirtualdisplay
import re
import selenium
from selenium.webdriver.common.by import By

class GetBusStop:
    def get_busstop(self, erea:str) -> list:
        # # 仮想ディスプレイの設定
        # display = pyvirtualdisplay.Display(visible=0, size=(1024, 768))
        # display.start()
        # ドライバの取得，URLにアクセス
        driver = self._start_webdriver()
        driver.get('https://www.navitime.co.jp/bus/diagram/busstop/22138/00001037/?name=') # 静岡県 浜松市中央区 全域
        # 指定した地域のバス停一覧を取得
        driver.find_element(By.ID, 'address-level-3').send_keys(erea)
        driver.find_element(By.ID, 'submit_busstop_search').click()
        elements = driver.find_elements(By.CSS_SELECTOR, '.node-list a')
        # バス停一覧を整形して保存
        result = {}
        busstops = [re.sub(r'\(.*?\)', '', element.text) for element in elements]
        result['busstops'] = busstops
        # ドライバ，ディスプレイを終了
        driver.quit()
        # display.stop()
        return [result]

    def _start_webdriver(self):
        # ドライバの設定
        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--single-process')
        options.add_argument('--proxy-server="direct://"')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--lang=ja')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = selenium.webdriver.Chrome(options=options)
        return driver

if __name__ == '__main__':
    getbusstop = GetBusStop()
    print(getbusstop.get_busstop('布橋'))