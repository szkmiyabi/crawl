import MySQLdb

conn = MySQLdb.connect(db="scraping", user="scraper", password="passwd", charset="utf8mb4")
c = conn.cursor()

c.execute("drop table if exists cities")

c.execute("""
create table cities (
    rank integer,
    city text,
    population integer
)
""")

c.execute("insert into cities values(%s, %s, %s)", (1,"上海", 24150000))
c.execute("insert into cities values(%(rank)s, %(city)s, %(population)s)",
{"rank": 2, "city":"カラチ", "population": 23500000})

c.executemany("insert into cities values(%(rank)s, %(city)s, %(population)s)", [
    {"rank":3 , "city":"北京" , "population":2151600 },
    {"rank":4 , "city":"天津" , "population":14722100 },
    {"rank":5 , "city":"イスタンブル" , "population":14160467 },
])

conn.commit()

c.execute("select * from cities")

for row in c.fetchall():
    print(row)

conn.close()