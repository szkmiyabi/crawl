from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from subprocess import Popen, PIPE
import time

options = Options()
options.binary_location = '/usr/bin/firefox'
# options.add_argument('-headless')
# unix-command: cat "$HOME/.mozilla/firefox/profiles.ini" | sed -n -e 's/^.*Path=//p' | head -n 1
profile_dir = '/home/vagrant/.mozilla/firefox/'
profile_fname = Popen('cat "$HOME/.mozilla/firefox/profiles.ini" | sed -n -e \'s/^.*Path=//p\' | head -n 1', shell=True, stdout=PIPE).communicate()[0].decode().strip()
profile_my_path = profile_dir + profile_fname
options.profile = profile_my_path
driver = webdriver.Firefox(firefox_options=options)

driver.get('https://www.google.co.jp/')
# elm = driver.find_element_by_tag_name("body")
# elm.send_keys(Keys.CONTROL, "a")
html = driver.page_source
time.sleep(10)
driver.save_screenshot("google.png")
print(html)

driver.quit()
