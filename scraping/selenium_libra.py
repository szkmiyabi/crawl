from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import datetime
import time
import yaml

class LibraRepBots:
    def __init__(self, projectID):
        with open("user.yaml") as f:
            userdata = yaml.load(f)
            self.uid = userdata["uid"]
            self.passwd = userdata["pswd"]
            self.systemWait = userdata["systemWait"]
        self.app_url = "https://accessibility.jp/libra/"
        self.index_url = "https://jis.infocreate.co.jp/"
        self.rep_index_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report/projID/"
        self.rep_detail_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report2/projID/"
        self.projectID = projectID
        self.wd = webdriver.PhantomJS()
        self.wd.implicitly_wait(self.systemWait)
        self.wd.set_window_size(1280, 900)
        self.wd.get(self.app_url)
    
    def getWd(self):
        return self.wd
    
    def login(self):
        self.wd.find_element_by_id("uid").send_keys(self.uid)
        self.wd.find_element_by_id("pswd").send_keys(self.passwd)
        self.wd.find_element_by_id("btn").click()

    def logout(self):
        self.wd.get(self.index_url)
        btnWrap = wd.find_element_by_id("btn")
        btnBase = btnWrap.find_element_by_tag_name("ul")
        btnBaseInner = btnBase.find_element_by_class_name("btn2")
        btnA = btnBaseInner.find_element_by_tag_name("a")
        btnA.click()
    
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

args = sys.argv
projectID = args[1]
lbt = LibraRepBots(projectID)
time.sleep(8)
lbt.login()
time.sleep(8)
lbt.view_report()
time.sleep(3)
lbt.save_sc()
lbt.logout
time.sleep(8)
lbt.shutdown()