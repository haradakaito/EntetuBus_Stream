import pyvirtualdisplay
import selenium
from selenium.webdriver.common.by import By
from datetime import datetime

class GetBusTime:
    def get_bustime(self, bus_from:str, bus_to:str) -> list:
        # 仮想ディスプレイの設定
        display = pyvirtualdisplay.Display(visible=0, size=(1024, 768))
        display.start()
        # ドライバの取得，URLにアクセス
        driver = self._start_webdriver()
        driver.get('https://info.entetsu.co.jp/navi/pc/annai.aspx')
        # バス時刻表を取得
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder2_TBusFrom').send_keys(bus_from)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder2_TBusTo').send_keys(bus_to)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder2_BtnSearch').click()
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder2_BtnResult').click()
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder2_LinkBusdokoFrom').click()
        driver.switch_to.window(driver.window_handles[1])
        # 取得日時を保存
        result = {}
        result['gettime'] = datetime.now().strftime('%Y/%m/%d %H:%M')
        # 運行状況を取得
        rows = driver.find_elements(By.XPATH, '//tbody/tr')
        tmp = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if cells[2].text != '通過':
                tmp.append([cells[1].text, cells[2].text])
        result['bustime'] = tmp
        # ドライバ，ディスプレイを終了
        driver.quit()
        display.stop()
        print(result)
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