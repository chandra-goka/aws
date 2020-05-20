from selenium import webdriver
import shutil
from selenium.webdriver.chrome.options import Options
import os
import time
import stat


def lambda_handler(event, context):
    # TODO implement
    print("Starting google.com")
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
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
    #chrome_options.add_argument('executable_path='+os.getcwd() + "/bin/headless-chromium")
    #_init_bin("headless-chromium")
    print("cwd : "+os.getcwd())
    driver = webdriver.Chrome(chrome_options=chrome_options)
    page_data = ""
    if 'url' in event.keys():
        driver.get(event['url'])
        page_data = driver.page_source
        print(page_data)
    driver.close()
    return page_data

CURR_BIN_DIR = os.getcwd() + "/bin/"
### In order to get permissions right, we have to copy them to /tmp
BIN_DIR = '/tmp/'

# This is necessary as we don't have permissions in /var/tasks/bin where the lambda function is running
def _init_bin(executable_name):
    start = time.clock()
    if not os.path.exists(BIN_DIR):
        print("Creating bin folder")
        os.makedirs(BIN_DIR)
    print("Copying binaries for "+executable_name+" in /tmp/")
    currfile = os.path.join(CURR_BIN_DIR,executable_name)
    print("Current File location : "+currfile)
    newfile  = os.path.join(BIN_DIR, executable_name)
    print("New File location : " + newfile)
    shutil.copy2(currfile, newfile)
    print("Giving new binaries permissions for lambda")
    os.chmod(newfile, 775)
    print("Checking permissions..")
    st = os.stat(newfile)
    oct_perm = oct(st.st_mode)
    print("Permission > "+oct_perm)
    elapsed = (time.clock() - start)
    print(executable_name+" ready in "+str(elapsed)+'s.')
