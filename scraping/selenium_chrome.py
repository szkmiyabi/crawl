from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from os.path import expanduser

user_dir = expanduser('~') 

ch_options = ChromeOptions()
ch_options.binary_location = '/usr/bin/google-chrome'

# /home/vagrant/.google/Defaultにする
ch_profile_dir = '--user-data-dir=' + user_dir + '/.google'
ch_options.add_argument(ch_profile_dir)
ch_wd = webdriver.Chrome(chrome_options=ch_options)

ch_wd.get('https://www.google.co.jp/')
html = ch_wd.page_source
time.sleep(10)
ch_wd.save_screenshot("google-chrome.png")
print(html)

ch_wd.quit()