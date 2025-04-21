from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from selenium.webdriver.chrome.service import Service
import os

class TestDisclosure():
    def test_disclosure1(self, driver, testdata):

        url = os.environ["URL"]+"/top"
        driver.get(url)
        driver.find_element(By.CSS_SELECTOR, ".c-check-box").click()
        driver.find_element(By.ID, "netEntryNo").send_keys(testdata["entryNo"])
        driver.find_element(By.ID, "tel").send_keys(testdata["tel"])
        driver.save_screenshot_with_case()
        driver.find_element(By.ID, "next").click()

        assert driver.current_url == url + "/disclosure"

        driver.save_screenshot_with_case()


    def test_disclosure2(self, driver, testdata):
        # 入力項目のIDとtestdataキーの対応表
        input_map = {
            "lastKana": "lastKana",
            "firstKana": "firstKana",
            "birthDateEra": "birthDateEra",
            "birthDateYear": "birthDateYear",
            "birthDateMonth": "birthDateMonth",
            "birthDateDay": "birthDateDay",
            "mailAddress": "mailAddress",
            "mailAddressCheck": "mailAddress",
            "creditCardNo1": "creditCardNo1",
            "creditCardNo2": "creditCardNo2",
            "creditCardNo3": "creditCardNo3",
            "creditCardNo4": "creditCardNo4",
            "userFullName": "userFullName",
            "securityCode": "securityCode"
        }

        for elem_id, data_key in input_map.items():
            driver.find_element(By.ID, elem_id).send_keys(testdata[data_key])

        # ラジオボタン（ラベル名で指定）
        driver.find_element(By.XPATH, f"//label[contains(.,'{testdata['creditguidance']}')]").click()

        driver.save_screenshot_with_case()
        driver.find_element(By.ID, "next").click()
        driver.save_screenshot_with_case()