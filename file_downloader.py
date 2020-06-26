from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os

LOGIN_URL = "https://otp.demo.com//login"
USER = "demo"
PASS = "demo"
download_dir = "/tmp/fr/"

def enable_download(browser):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def setting_chrome_options():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
    return chrome_options;

def lambda_handler(event, context):
    day = datetime.today().strftime('%Y%m%d')
    DOWNLOAD_URL = "https://otp.demo.com/domain-names-{}.{}".format(day,"zip")
    driver = webdriver.Chrome(options=setting_chrome_options())
    print("loading URL")
    driver.get(LOGIN_URL)
    print("Loaded URL")
    driver.find_element_by_id("login_username").send_keys(USER)
    driver.find_element_by_id("login_password").send_keys(PASS)
    print("Before Login click")
    driver.find_element_by_class_name("authentication_btn").click()
    enable_download(driver)
    time.sleep(10)
    print("After sleep..")
    driver.get(DOWNLOAD_URL)
    time.sleep(20)
    file_path = "/tmp/fr/domain-names-{}.{}".format(day,"zip")
    while not os.path.exists(file_path):
        time.sleep(10)
    if os.path.isfile(file_path):
        print("File has been downloaded at "+file_path)
    else:
        raise ValueError("%s isn't a file!" % file_path)
    print("After download complete..")
    return "success"

