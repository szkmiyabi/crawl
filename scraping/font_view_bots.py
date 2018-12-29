from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from subprocess import Popen, PIPE
import time
import os
from os.path import expanduser
import datetime
import sys
import argparse
import textwrap

class FontViewBots:
    def __init__(self, projectID, urls_filename, headless_flag=False):
        self.projectID = projectID
        self.urls_filename = urls_filename
        self.headless_flag = headless_flag
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
        if self.headless_flag is True:
            options.add_argument('-headless')
        else:
            pass
        return options
    
    def get_ch_options(self):
        options = ChromeOptions()
        options.binary_location = self.ch_path
        profile_dir = '--user-data-dir=' +self. user_dir + '/.google'
        options.add_argument(profile_dir)
        if self.headless_flag is True:
            options.add_argument('--headless')
        else:
            pass
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
    
    def  fullpage_screenshot(self, driver, path):
        original_size = driver.get_window_size()
        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        # driver.save_screenshot(path)  # has scrollbar
        driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
        driver.set_window_size(original_size['width'], original_size['height'])

    def exec(self):
        datas = self.load_url_datas()
        save_path = self.get_save_directory()
        fxwd = self.open_fx_wd()
        for r in datas:
            pid = r["pid"]
            url = r["url"]
            print("firefox: ", pid, " を処理しています。")
            fxwd.get(url)
            time.sleep(self.shortWait)
            self.fullpage_screenshot(fxwd, save_path + "/firefox/fx_" + pid + ".png")
        self.close_wd(fxwd)
        chwd = self.open_ch_wd()
        for r in datas:
            pid = r["pid"]
            url = r["url"]
            print("chrome:  ", pid, " を処理しています。")
            chwd.get(url)
            time.sleep(self.shortWait)
            self.fullpage_screenshot(chwd, save_path + "/chrome/ch_" + pid + ".png")
        self.close_wd(chwd)


params = argparse.ArgumentParser(
    usage='%(prog)s [arg1] [arg2]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''
        note:
        始めに以下の設定を行うこと
        # Firefoxを起動しデフォルトフォントサイズを16ptから32ptに変更する
        # Chromeを以下のコマンドで起動しデフォルトフォントサイズを16ptから32ptに変更する
        $ google-chrome --user-data-dir=/home/vagrant/.google
    ''')
)
params.add_argument('arg1', help='input the projectID')
params.add_argument('arg2', help='input the URLs file name')
args = params.parse_args()

projectID = args.arg1
urls_filename = args.arg2
app = FontViewBots(projectID, urls_filename)
app.exec()
