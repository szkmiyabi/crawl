from bayberry_bots import BayBerryBots
import time

bbt = BayBerryBots()
time.sleep(bbt.midWait)
bbt.login()
time.sleep(bbt.midWait)

bbt.go_sitemap()
time.sleep(bbt.midWait)

bbt.go_sitemap_articles_list()
time.sleep(bbt.midWait)

bbt.preview_page_screen_shot(0)

bbt.logout()
time.sleep(bbt.midWait)

bbt.shutdown()