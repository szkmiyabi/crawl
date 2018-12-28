from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from subprocess import Popen, PIPE
import time
import os
from os.path import expanduser
import datetime

class FontViewBots:
    def __init__(self, projectID, urls_filename):
        self.projectID = projectID
        self.urls_filename = urls_filename
        self.shortWait = 1
        self.midWait = 3
        self.longWait = 10
        self.user_dir = expanduser('~')
        self.fx_path = '/usr/bin/firefox'
        self.ch_path = '/usr/bin/google-chrome'

    def get_fx_options(self):
        options = FirefoxOptions()
        options.binary_location = self.fx_path
        profile_dir = self.user_dir + '/.mozilla/firefox/'
        profile_fname = Popen('cat "$HOME/.mozilla/firefox/profiles.ini" | sed -n -e \'s/^.*Path=//p\' | head -n 1', shell=True, stdout=PIPE).communicate()[0].decode().strip()
        options.profile = profile_dir + profile_fname
        return options
    
    def get_ch_options(self):
        options = ChromeOptions()
        options.binary_location = self.ch_path
        profile_dir = '--user-data-dir=' +self. user_dir + '/.google'
        options.add_argument(profile_dir)
        return options
    
    def open_fx_wd(self):
        return webdriver.Firefox(firefox_options=self.get_fx_options())
    
    def open_ch_wd(self):
        return webdriver.Chrome(chrome_options=self.get_ch_options())

    def close_wd(self, wd):
        wd.quit()

    def load_url_datas(self):
        datas = []
        with open(self.urls_filename, "r") as f:
            for r in f:
                line = r.strip()
                cols = line.split("\t")
                datas.append({"pid": cols[0], "url": cols[1]})
        return datas

    def get_uniq_file_name(self, ext_str):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + ext_str

    def get_uniq_dir_name(self):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y%m%d-%H%M%S") 
    
    def get_save_directory(self):
        save_path = self.projectID + "-" + self.get_uniq_dir_name()
        os.makedirs(save_path + "/firefox", exist_ok=True)
        os.makedirs(save_path + "/chrome", exist_ok=True)
        return save_path + "/"

    def exec(self):
        save_path = self.get_save_directory()
        fxwd = self.open_fx_wd()
        fxwd.get("https://www.google.co.jp/")
        fxwd.save_screenshot(save_path + "/firefox/capture.png")
        time.sleep(self.shortWait)
        self.close_wd(fxwd)

        chwd = self.open_ch_wd()
        chwd.get("https://www.google.co.jp/")
        chwd.save_screenshot(save_path + "/chrome/capture.png")
        time.sleep(self.shortWait)
        self.close_wd(chwd)

app = FontViewBots("474", "test")
app.exec()
