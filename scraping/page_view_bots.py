from selenium import webdriver
from subprocess import Popen, PIPE
import time
import os
from os.path import expanduser
import datetime
import sys
import argparse
from PIL import Image
import shutil

class PageViewBots:
    def __init__(self, projectID, urls_filename):
        self.projectID = projectID
        self.urls_filename = urls_filename
        self.shortWait = 1
        self.midWait = 3
        self.longWait = 10
        self.user_dir = expanduser('~')
        self.extends_screenshot_wait = 1

    def get_pjs_options(self):
        pass

    def open_pjs_wd(self):
        wd = webdriver.PhantomJS()
        wd.set_window_size(1280, 900)
        return wd

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
        os.makedirs(save_path + "/phantomJS", exist_ok=True)
        return save_path + "/"
    
    def  fullpage_screenshot(self, browser_name, driver, path):
        if browser_name == "phantomJS":
            original_size = driver.get_window_size()
            required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(required_width, required_height)
            driver.find_element_by_tag_name('body').screenshot(path)
            driver.set_window_size(original_size['width'], original_size['height'])
        else:
            pass

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

    def exec_phantomjs(self, datas, save_path):
        pjswd = self.open_pjs_wd()
        for r in datas:
            pid = r["pid"]
            url = r["url"]
            print("phantomJS: ", pid, " を処理しています。")
            pjswd.get(url)
            time.sleep(self.shortWait)
            self.fullpage_screenshot("phantomJS", pjswd, save_path + "/phantomJS/pjs_" + pid + ".png")
        self.close_wd(pjswd)

    def exec(self):
        datas = self.load_url_datas()
        save_path = self.get_save_directory()
        self.exec_phantomjs(datas, save_path)


params = argparse.ArgumentParser(usage='%(prog)s [arg1] [arg2]')
params.add_argument('arg1', help='input the projectID')
params.add_argument('arg2', help='input the URLs file name')
args = params.parse_args()

projectID = args.arg1
urls_filename = args.arg2
app = PageViewBots(projectID, urls_filename)
app.exec()
