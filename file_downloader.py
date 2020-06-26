from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

download_dir = "/tmp/downloads/"

def enable_download(browser):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def isFileDownloaded():
    file_path = download_dir+"/python_samples-master.zip"
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.isfile(file_path):
        print("File Downloaded successfully..")

def setting_chrome_options():
    chrome_options = Options()
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
    print("Started Lambda..")
    DOWNLOAD_URL = "https://github.com/chandrashekhargoka/python_samples/archive/master.zip"
    driver = webdriver.Chrome(options=setting_chrome_options())
    driver.get(DOWNLOAD_URL)
    isFileDownloaded()
    return "success"

