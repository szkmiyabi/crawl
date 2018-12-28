from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.keys import Keys
from subprocess import Popen, PIPE
import time
from os.path import expanduser

user_dir = expanduser('~')

fx_options = FirefoxOptions()
fx_options.binary_location = '/usr/bin/firefox'

# options.add_argument('-headless')
# unix-command: cat "$HOME/.mozilla/firefox/profiles.ini" | sed -n -e 's/^.*Path=//p' | head -n 1
fx_profile_dir = user_dir + '/.mozilla/firefox/'
fx_profile_fname = Popen('cat "$HOME/.mozilla/firefox/profiles.ini" | sed -n -e \'s/^.*Path=//p\' | head -n 1', shell=True, stdout=PIPE).communicate()[0].decode().strip()
fx_options.profile = fx_profile_dir + fx_profile_fname
fx_wd = webdriver.Firefox(firefox_options=fx_options)

fx_wd.get('https://www.google.co.jp/')
# elm = fx_wd.find_element_by_tag_name("body")
# elm.send_keys(Keys.CONTROL, "a")
html = fx_wd.page_source
time.sleep(10)
fx_wd.save_screenshot("google.png")
print(html)

fx_wd.quit()
