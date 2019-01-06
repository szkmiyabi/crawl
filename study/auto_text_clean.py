import sys
import os
import re
from glob import glob

def text_clean(content):
    pt1 = re.compile(r'-{2,} Page [0-9]+-{2,}', re.DOTALL)
    pt2 = re.compile(r'^\s+', re.DOTALL)
    pt3 = re.compile(r' +$', re.DOTALL)
    pt4 = re.compile(r'\s{2,}', re.DOTALL)
    content = re.sub(pt1, "", content)
    content = re.sub(pt2, "", content)
    content = re.sub(pt3, "", content)
    content = re.sub(pt4, "", content)
    return content

for path in glob(os.path.join("text", "*.txt")):
    with open(path, "r") as f1:
        tmpdata = f1.read()
    tmpdata = text_clean(tmpdata)
    print(tmpdata)
    with open(path, "w") as f2:
        f2.write(tmpdata)

