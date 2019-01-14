from bayberry_bots import BayBerryBots
import time

bbt = BayBerryBots()
time.sleep(bbt.midWait)
bbt.login()
time.sleep(bbt.midWait)

bbt.go_sitemap()
time.sleep(bbt.midWait)

bbt.select_site()
time.sleep(bbt.midWait)

bbt.go_sitemap_articles_list()
time.sleep(bbt.midWait)

bbt.write_article_datas()
bbt.logout()
time.sleep(bbt.midWait)

bbt.shutdown()