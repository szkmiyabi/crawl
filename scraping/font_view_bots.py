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
from PIL import Image
import shutil

class FontViewBots:
    def __init__(self, projectID, urls_filename, operation_flag, headless_flag=False):
        self.projectID = projectID
        self.urls_filename = urls_filename
        self.operation_flag = operation_flag
        self.headless_flag = headless_flag
        self.shortWait = 1
        self.midWait = 3
        self.longWait = 10
        self.user_dir = expanduser('~')
        self.fx_path = '/usr/bin/firefox'
        self.ch_path = '/usr/bin/google-chrome'
        self.extends_screenshot_wait = 1

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
        if self.operation_flag == "all" or self.operation_flag == "firefox":
            os.makedirs(save_path + "/firefox", exist_ok=True)
        if self.operation_flag == "all" or self.operation_flag == "chrome":
            os.makedirs(save_path + "/chrome", exist_ok=True)
        return save_path + "/"
    
    def  fullpage_screenshot(self, browser_name, driver, path):
        if browser_name == "firefox":
            self.extends_save_screenshot(driver, path)
        elif browser_name == "chrome":
            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element_by_tag_name('body').screenshot(path)
            driver.set_window_size(original_size['width'], original_size['height'])

    def extends_save_screenshot(self, wd, filename):
        filepath = '/'.join(filename.split('/')[:-1])
        tmpdirpath = filepath + "/tmp"
        os.makedirs(tmpdirpath)
        print("一時ディレクトリ:", tmpdirpath, "を作成しました。")
        wd.execute_script("window.scrollTo(0, 0);")
        total_width = wd.execute_script("return document.body.scrollWidth")
        total_height = wd.execute_script("return document.body.scrollHeight")
        view_width = wd.execute_script("return window.innerWidth")
        view_height = wd.execute_script("return window.innerHeight")

        stitched_image = Image.new("RGB", (total_width, total_height))
        scroll_width = 0
        scroll_height = 0
        row_count = 0

        while scroll_height < total_height:
            col_count = 0
            scroll_width = 0
            wd.execute_script("window.scrollTo(%d, %d)" % (scroll_width, scroll_height))

            while scroll_width < total_width:
                if col_count > 0:
                    wd.execute_script("window.scrollBy(" + str(view_width) + ", 0)")
                tmpname = filepath + '/tmp/tmp_%d_%d.png' % (row_count, col_count)
                wd.save_screenshot(tmpname)
                print(tmpname, "を一時的に保存しました。")
                time.sleep(self.extends_screenshot_wait)

                if scroll_width + view_width >= total_width or scroll_height + view_height >= total_height:
                    new_width = view_width
                    new_height = view_height
                    if scroll_width + view_width >= total_width:
                        new_width = total_width - scroll_width
                    if scroll_height + view_height >= total_height:
                        new_height = total_height - scroll_height
                    tmp_image = Image.open(tmpname)
                    tmp_image.crop((view_width - new_width, view_height - new_height, view_width, view_height)).save(tmpname)
                    stitched_image.paste(Image.open(tmpname), (scroll_width, scroll_height))
                    scroll_width += new_width

                else:
                    stitched_image.paste(Image.open(tmpname), (scroll_width, scroll_height))
                    scroll_width += view_width
                    col_count += 1

            scroll_height += view_height
            time.sleep(self.extends_screenshot_wait)

        stitched_image.save(filename)
        shutil.rmtree(tmpdirpath)
        print("一時ディレクトリ:", tmpdirpath, " を削除しました。")

    def exec_firefox(self, datas, save_path):
        fxwd = self.open_fx_wd()
        for r in datas:
            pid = r["pid"]
            url = r["url"]
            print("firefox: ", pid, " を処理しています。")
            fxwd.get(url)
            time.sleep(self.shortWait)
            self.fullpage_screenshot("firefox", fxwd, save_path + "/firefox/fx_" + pid + ".png")
        self.close_wd(fxwd)

    def exec_chrome(self, datas, save_path):
        chwd = self.open_ch_wd()
        for r in datas:
            pid = r["pid"]
            url = r["url"]
            print("chrome:  ", pid, " を処理しています。")
            chwd.get(url)
            time.sleep(self.shortWait)
            self.fullpage_screenshot("chrome", chwd, save_path + "/chrome/ch_" + pid + ".png")
        self.close_wd(chwd)

    def exec(self):
        datas = self.load_url_datas()
        save_path = self.get_save_directory()
        if self.operation_flag == "all":
            self.exec_firefox(datas, save_path)
            self.exec_chrome(datas, save_path)
        elif self.operation_flag == "firefox":
            self.exec_firefox(datas, save_path)
        elif self.operation_flag == "chrome":
            self.exec_chrome(datas, save_path)


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
params.add_argument('arg3', help='choose value in [all,firefox,chrome]')
args = params.parse_args()

projectID = args.arg1
urls_filename = args.arg2
operation_flag = args.arg3
app = FontViewBots(projectID, urls_filename, operation_flag)
app.exec()
