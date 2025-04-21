import pytest
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome import service as chrome_fs
from selenium.webdriver.edge import service as edge_fs
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import base64
from dotenv import load_dotenv
import json
import sys
from selenium.webdriver.common.by import By

load_dotenv()

@pytest.fixture(scope="class")
def driver(request):
    browser = os.environ.get("browser_type")
    headlessflg = os.environ.get("headless_mode")
    width = os.environ.get("window_width")
    height = os.environ.get("window_height")


    if browser == "Edge":
        options = EdgeOptions()
    elif browser == "Chrome":
        options = ChromeOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    if headlessflg and headlessflg.lower() in ['true', '1', 'yes']:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-desktop-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--lang=ja")

    driver = None
    try:
        if browser == "Edge":
            driver = webdriver.Edge(options=options)
        elif browser == "Chrome":
            driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Error: {e}")
    
    driver.set_window_size(width, height)
    driver.implicitly_wait(10)

    # カスタムメソッドを追加
    def save_screenshot_with_case():
        # 環境変数取得
        screenshot_config = bool(os.environ.get("is_full_size"))

        # 呼び出し元のクラス名とメソッド名を取得
        frame = sys._getframe(1)
        casename = frame.f_code.co_name
        caller = frame.f_locals.get("self", None)
        if caller is not None:
            class_name = caller.__class__.__name__
        else:
            class_name = "default_directory"

        # ディレクトリ作成
        base_dir = os.path.join("..", "screenshot")
        class_dir = os.path.join(base_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)

        # ファイル名生成（メソッド名_連番.png）
        count = 1
        file_path = os.path.join(class_dir, f"{casename}_{count}.png")
        while os.path.exists(file_path):
            count += 1
            file_path = os.path.join(class_dir, f"{casename}_{count}.png")

        # スクリーンショットを保存（フルページ or 通常）
        if screenshot_config and hasattr(driver, "execute_cdp_cmd"):
            # フルページキャプチャ（Chromeのみ対応）
            params = {"captureBeyondViewport": True}
            base64_image = driver.execute_cdp_cmd("Page.captureScreenshot", params)
            with open(file_path, "wb") as fh:
                fh.write(base64.urlsafe_b64decode(base64_image["data"]))
        else:
            # 通常のスクリーンショット
            driver.save_screenshot(file_path)
    driver.save_screenshot_with_case = save_screenshot_with_case
    

    yield driver

    if driver:
        driver.quit()


@pytest.fixture(scope="class")
def testdata(request):
    #casename = request.node.name
    class_name = request.cls.__name__ if request.cls else ""

    with open(os.path.join("..", "json","testconf.json"), encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item["testcase"] == class_name:
            # クレジットガイダンスを変換
            if item["detail"]["creditguidance"] == 0:
                item["detail"]["creditguidance"] = os.environ.get("creditGuidanceOff")
            elif item["detail"]["creditguidance"] == 1:
                item["detail"]["creditguidance"] = os.environ.get("creditGuidanceOn")
            else:pytest.fail("クレジットガイダンスはなんとなく数値型にしているので0または1を指定してください")

            return item["detail"]
    pytest.fail("テストデータが見つかりません")

