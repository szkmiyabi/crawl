from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.alert import Alert
import sys
import datetime
import time
import yaml
from subprocess import Popen, PIPE
import os
from os.path import expanduser
import shutil
from PIL import Image
import lxml.html
import html
import re


class BayBerryBots:
    def __init__(self):
        with open("user.yaml") as f:
            userdata = yaml.load(f)
            self.bsid = userdata["bsid"]
            self.bspswd = userdata["bspswd"]
            self.uid = userdata["uid"]
            self.passwd = userdata["pswd"]
            self.systemWait = userdata["systemWait"]
            self.shortWait = userdata["shortWait"]
            self.midWait = userdata["midWait"]
            self.longWait = userdata["longWait"]
        self.app_url = "http://183.176.243.154/cms/"
        self.user_dir = expanduser('~')
        self.fx_path = '/usr/bin/firefox'
        self.ch_path = '/usr/bin/google-chrome'
        self.articles_file = "articles.txt"
        self.sc_save_path = "pref-shiga"
        self.extends_screenshot_wait = 1
        self.wd = webdriver.Firefox(firefox_options=self.get_fx_options())
        self.wd.implicitly_wait(self.systemWait)
        self.wd.set_window_size(1280, 900)
        self.wd.get(self.app_url)
        alert = self.wd.switch_to_alert()
        alert.send_keys(self.bsid + Keys.TAB + self.bspswd)
        alert.accept()

    def getWd(self):
        return self.wd

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

    def login(self):
        self.wd.find_element_by_id("number").send_keys(self.uid)
        self.wd.find_element_by_id("password").send_keys(self.passwd)
        self.wd.find_element_by_css_selector(".submit input").click()

    def logout(self):
        self.go_sitemap()
        time.sleep(self.midWait)
        btn = self.wd.find_element_by_css_selector(".top-bar-section ul.right li:nth-child(3)")
        btn.click()

    def shutdown(self):
        self.wd.quit()

    def select_site(self):
        ddl = self.wd.find_element_by_id("site-groups")
        for opt in ddl.find_elements_by_tag_name("option"):
            optval = opt.get_attribute("value")
            opttxt = opt.text
            if optval == "1" and opttxt.strip() == "滋賀県ホームページ":
                opt.click()
                break

    def go_sitemap(self):
        self.wd.get(self.app_url + "site_maps/frame")
    
    def go_sitemap_articles_list(self):
        self.wd.find_element_by_xpath("/html/body/div[1]/div/div[2]/ul/li/ul/li[1]/a[4]").click()
    
    def get_dom(self):
        html_str = self.wd.page_source
        return lxml.html.fromstring(html_str)

    def fetch_articles_data(self):
        datas = []
        dom = self.get_dom()
        ul = dom.xpath("/html/body/div[1]/div/div/ul/li/ul")[0]
        for row in ul.cssselect("li"):
            li = lxml.html.tostring(row).decode()
            lidom = lxml.html.fromstring(li)
            irows = lidom.cssselect("a")
            datas.append({
                "pid": self.get_pageID(irows[0].get("href")),
                "pname": irows[0].text
            })
        return datas

    def load_articles_data(self):
        datas = []
        with open(self.articles_file, "r") as f:
            line = [s.strip() for s in f.readlines()]
            for r in line:
                tmp = r.split("\t")
                datas.append({
                    "pid": tmp[0],
                    "pname": tmp[1]
                })
        return datas

    def get_pageID(self, href_val):
        return re.search(r'\?id=(.+)', href_val).group(1)
    
    def preview_page_screen_shot(self, max_limit):
        datas = self.load_articles_data()
        url_base = self.app_url + "article_pages/preview?id="
        cnt = 0
        for row in datas:
            if max_limit is not 0 and cnt > max_limit:
                break
            pid = row["pid"]
            pname = row["pname"]
            print(pid, " ", pname, " を処理しています。")
            self.wd.get(url_base + pid)
            time.sleep(self.shortWait)
            self.fullpage_screenshot("firefox", self.wd, self.sc_save_path + pid + "_" + pname + ".png")
            cnt += 1

    def fetch_filename_from_datetime(self, ext_str):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + ext_str

    def pass_basic_auth(self):
        jstxt = "var XMLReq = new XMLHttpRequest();"
        jstxt += "XMLReq.open('GET', '"
        jstxt += self.app_url + "', false, '"
        jstxt += self.bsid + "', '"
        jstxt += self.bspswd + "');"
        jstxt += "XMLReq.send(null);"
        self.wd.execute_script(jstxt)

    def get_uniq_file_name(self, ext_str):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + ext_str

    def get_uniq_dir_name(self):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y%m%d-%H%M%S") 
    
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
        if not os.path.exists(tmpdirpath):
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
