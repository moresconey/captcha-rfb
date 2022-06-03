import os
import pkg_resources
import subprocess
import json
import platform
from time import sleep

required = {'numpy', 'selenium', 'scipy', 'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
for pkg in missing:
    os.system(f'pip install {pkg}')

import requests
import numpy as np
from io import BytesIO
from scipy.io import wavfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class RFBElements:
    URLmain = 'http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao_CS.asp'
    URLwave = 'http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/captcha/gerarSom.asp'

    BTSearch = (By.XPATH, '//*[@id="frmConsulta"]/div[3]/div/button[1]')
    INPUTCnpj = (By.XPATH, '//*[@id="cnpj"]')
    INPUTCaptcha = (By.XPATH, '//*[@id="txtTexto_captcha_serpro_gov_br"]')

    DIVContent = (By.ID, 'principal')
    CSSPrint = "<link href='http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/css/print.css' rel='stylesheet' type='text/css' />"
    IMAGEBrasao = 'http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/images/brasao2.gif'

class RFB_CNPJ:
    def __init__(self) -> None:
        self.chromePath = 'chromedriver/chromedriver.exe'
        self.header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
        self.driver = None

        with open('data/digits.json') as f:
            self.digitsData = json.load(f)

        if platform.system() == 'Darwin':
            self.copy_keyword = 'pbcopy'
        elif platform.system() == 'Windows':
            self.copy_keyword = 'clip'

    def config(self, chromePath):
        self.chromePath = chromePath

    def _paste_text(self, value):
        subprocess.run(self.copy_keyword, universal_newlines=True, input=value)
        ActionChains(self.driver).key_down(Keys.CONTROL).key_down('v').key_up('v').key_up(Keys.CONTROL).perform()

    def _start_chrome(self, show):
        chromeOptions = webdriver.ChromeOptions()

        if not show:
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--no-sandbox')
        
        driver = webdriver.Chrome(self.chromePath, chrome_options=chromeOptions)

        self.driver = driver

    def _download_wave(self, first_try = True):
        if first_try:
            sleep(2)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(RFBElements.INPUTCaptcha))

        cookie_dict = {}
        for cookie in self.driver.get_cookies():
            cookie_dict[cookie['name']] = cookie['value']

        header = self.header

        r = requests.get(RFBElements.URLwave, cookies= cookie_dict, headers = header)
        
        if r.content == b'':
            if not first_try:
                print('Error: Failed to download wave file, please reload the page!')
                self.driver.refresh()
                return False
            else:
                self._download_wave(first_try=False)
        else:
            self.wave_rate, self.wave_data = wavfile.read(BytesIO(r.content))
            return True

    def _remove_noise(self, data, acc = .4, steps = 500):
        x = data.copy()
        last = 0
        for idx in range(steps, len(x), steps):
            dist = len(set(x[last:idx])) / len(x[last:idx])
            if dist > acc and dist < .91:
                x[last:idx] = self._remove_noise(x[last:idx], steps = int(steps/2))
            if dist < acc:
                x[last:idx] = 0
            last = idx
        return x

    def _find_letters(self, x, limit = 100):
        letters = []
        letter = False
        zeros = 0
        for idx, value in enumerate(x):
            if value != 0 and letter == False:
                start = idx
                letter = True
                zeros = 0
            elif value == 0 and letter:
                zeros += 1

            if (zeros > limit and letter) or (idx == len(x)-1):
                if (idx-limit) - start >= 2000:
                    letters.append(x[start:idx-limit])
                letter = False

        return letters

    def _solve_captcha(self):
        new_data = self._remove_noise(self.wave_data)
        limit = 100
        ar_letters = 'letters'
        while len(ar_letters) > 6:
            limit += 50
            ar_letters = self._find_letters(new_data, limit = limit)

        r = ''
        for letter in ar_letters:
            maxs = sorted(letter, reverse=True)[:100]
            mins = sorted(letter)[:100]

            for key, values in self.digitsData.items():
                if (np.std(np.array(values['maxs']) - np.array(maxs)) < 10) or (np.std(np.array(values['mins']) - np.array(mins)) < 10):
                    r += key
                    break
        return r

    def _save(self, cnpj):
        with open(f'Comprovante_{cnpj}.html', 'w+') as f:
            f.write(RFBElements.CSSPrint + self.driver.find_element(*RFBElements.DIVContent).get_attribute('innerHTML').replace('images/brasao2.gif',RFBElements.IMAGEBrasao))

    def get(self, cnpj, show = False):
        if self.driver is None:
            self._start_chrome(show)
        
        self.driver.get(RFBElements.URLmain)

        if self._download_wave():
            self.driver.find_element(*RFBElements.INPUTCaptcha).click()
            self._paste_text(self._solve_captcha())

            self.driver.find_element(*RFBElements.INPUTCnpj).click()
            self._paste_text(cnpj)

            self.driver.find_element(*RFBElements.BTSearch).click()

            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(RFBElements.DIVContent))
            self._save(cnpj)

        else:
            return False

if __name__ == '__main__':
    cnpj = RFB_CNPJ()
    cnpj.get('00000000000191', show = True)

