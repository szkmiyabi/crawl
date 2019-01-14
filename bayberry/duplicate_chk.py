
datas = []
with open("articles.txt", "r", encoding="utf-8") as f:
    line = [s.strip() for s in f.readlines()]
    for r in line:
        tmp = r.split("\t")
        datas.append(tmp[1])

duplicate_datas = [x for x in set(datas) if datas.count(x) > 1]

with open("duplicates.txt", "w", encoding="utf-8") as f:
    for r in duplicate_datas:
        f.write(r + "\n")


