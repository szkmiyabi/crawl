from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import sys
import datetime
import time
import yaml
from subprocess import Popen, PIPE
import os
from os.path import expanduser
import shutil

class BayBerryBots:
    def __init__(self):
        with open("user.yaml") as f:
            userdata = yaml.load(f)
            self.bsid = userdata["bsid"]
            self.bspswd = userdata["bspswd"]
            self.uid = userdata["uid"]
            self.passwd = userdata["pswd"]
            self.systemWait = userdata["systemWait"]
        self.auth = self.bsid +  ":" + self.bspswd + "@"
        self.app_url = "http://" + auth + "183.176.243.154/cms/"
        self.user_dir = expanduser('~')
        self.ch_path = '/usr/bin/google-chrome'
        self.wd = webdriver.Chrome()
        self.wd.implicitly_wait(self.systemWait)
        self.wd.set_window_size(1280, 900)
        self.wd.get(self.app_url)
    
    def getWd(self):
        return self.wd
    
    def login(self):
        self.wd.find_element_by_id("number").send_keys(self.uid)
        self.wd.find_element_by_id("password").send_keys(self.passwd)
        self.wd.find_element_by_css_selector(".submit input").click()

    def logout(self):
        btn = self.wd.find_element_by_css_selector(".top-bar-section ul.right li:nth-child(3)")
        btn.click()

    def shutdown(self):
        self.wd.quit()
    
    def save_sc(self):
        self.wd.save_screenshot(self.fetch_filename_from_datetime(".png"))

    def browse_rep(self):
        self.wd.get(self.rep_index_url_base + self.projectID)

    def fetch_filename_from_datetime(self, ext_str):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + ext_str
    
    def view_report(self):
        self.wd.get(self.rep_index_url_base + self.projectID + "/")

bbt = BayBerryBots()
bbt.save_sc()
time.sleep(8)
bbt.login()
time.sleep(8)
bbt.save_sc()
bbt.logout
time.sleep(8)
bbt.save_sc()
bbt.shutdown()