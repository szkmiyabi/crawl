from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import datetime
import time
import yaml
import lxml.html
import html
import re

class LibraRepBots:
    def __init__(self, projectID):
        with open("user.yaml") as f:
            userdata = yaml.load(f)
            self.uid = userdata["uid"]
            self.passwd = userdata["pswd"]
            self.systemWait = userdata["systemWait"]
            self.longWait = userdata["longWait"]
            self.midWait = userdata["midWait"]
            self.shortWait = userdata["shortWait"]
        self.app_url = "https://accessibility.jp/libra/"
        self.index_url = "https://jis.infocreate.co.jp/"
        self.rep_index_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report/projID/"
        self.rep_detail_url_base = "http://jis.infocreate.co.jp/diagnose/indexv2/report2/projID/"
        self.guideline_filename = "guideline_datas.txt"
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
    
    def save_sc(self, filename):
        self.wd.save_screenshot(filename)

    def browse_rep(self):
        self.wd.get(self.rep_index_url_base + self.projectID)

    def fetch_filename_from_datetime(self, ext_str):
        datetime_fmt = datetime.datetime.today()
        return datetime_fmt.strftime("%Y-%m-%d_%H-%M-%S") + ext_str
    
    def fetch_report_detail_path(self, pageID, guidelineID):
        return self.rep_detail_url_base + self.projectID + "/controlID/" + pageID + "/guideline/" + guidelineID + "/"

    def get_dom(self):
        html_str = self.wd.page_source
        return lxml.html.fromstring(html_str)
    
    def get_page_list_data(self):
        datas = []
        dom = self.get_dom()
        tbl = dom.xpath("/html/body/div[2]/div[1]/table")[0]
        for row in tbl.cssselect("tr td:first-child"):
            td_val = row.text
            datas.append(td_val)
        return datas
    
    def get_detail_table_data(self, pageID):
        datas = []
        dom = self.get_dom()
        tbl = dom.xpath("/html/body/div[2]/div[2]/table")[0]
        cnt = 0
        for row in tbl.cssselect("tr"):
            cnt += 1
            if cnt < 2:
                pass
            else:
                tr = html.unescape(lxml.html.tostring(row).decode())
                trdom = lxml.html.fromstring(tr)
                row_text = pageID + ","
                for irow in trdom.cssselect("td"):
                    td_val = irow.text
                    if td_val is None:
                        if self.is_including_tag(irow) is True:
                            row_text += self.get_regx_text(irow) + ","
                        else:
                            row_text += ","
                    else:
                        row_text += td_val.strip() + ","
                print(row_text)
                datas.append(row_text)
        return datas
    
    def is_including_tag(self, elm):
        tag_str = html.unescape(lxml.html.tostring(elm).decode())
        if re.search(r'<td.*?>(.+?)</td>', tag_str.strip(), re.DOTALL):
            return True
        else:
            return False

    def get_regx_text(self, elm):
        tag_str = html.unescape(lxml.html.tostring(elm).decode())
        tag_str = re.sub(r'(\r|\n|\r\n|\t|\s{2,})', "", tag_str)
        return re.search(r'<td.*?>(.+\!*?)</td>', tag_str.strip(), re.DOTALL).group(1)

    def open_text_data(self, filename):
        line = []
        with open(filename) as f:
            line = [s.strip() for s in f.readlines()]
        return line
    
    def save_text(self, text_data):
        with open(self.fetch_filename_from_datetime(".txt"), "w") as f:
            f.write(text_data)


class LibraRepBotsUtil(LibraRepBots):

    def fetch_report_sequential(self, guideline_arr):
        result_text = ""
        self.wd.get(self.rep_index_url_base + self.projectID + "/")
        if guideline_arr is None:
            guideline_rows = self.open_text_data(self.guideline_filename)
        else:
            guideline_rows = guideline_arr
        page_rows = self.get_page_list_data()
        for guideline in guideline_rows:
            for pageID in page_rows:
                print(pageID, ",", guideline, "を処理しています。")
                path = self.fetch_report_detail_path(pageID, guideline)
                self.wd.get(path)
                time.sleep(self.shortWait)
                for line in self.get_detail_table_data(pageID):
                    result_text += line + "\n"
                #self.save_sc(pageID + "_" + guideline + ".png")
        self.save_text(result_text)

    

args = sys.argv
projectID = args[1]
techID = args[2]
lbt = LibraRepBotsUtil(projectID)
time.sleep(lbt.shortWait)
lbt.login()
time.sleep(lbt.shortWait)
lbt.fetch_report_sequential([techID])
time.sleep(lbt.shortWait)
lbt.logout
time.sleep(lbt.shortWait)
lbt.shutdown()