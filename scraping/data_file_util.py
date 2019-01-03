import sys
import argparse
import re
import datetime
import time

class DataFileUtil:
    def __init__(self, operation_flag):
        self.operation_flag = operation_flag
        self.guideline_datas_file = "guideline_datas.txt"

    def reset_guideline_datas(self, level_flag):
        datas = []
        hashA = ["7.1.1.1","7.1.2.1","7.1.2.2","7.1.2.3","7.1.3.1","7.1.3.2","7.1.3.3","7.1.4.1","7.1.4.2","7.2.1.1","7.2.1.2","7.2.2.1","7.2.2.2","7.2.3.1","7.2.4.1","7.2.4.2","7.2.4.3","7.2.4.4","7.3.1.1","7.3.2.1","7.3.2.2","7.3.3.1","7.3.3.2","7.4.1.1","7.4.1.2"]
        hashAA = ["7.1.2.4","7.1.2.5","7.1.4.3","7.1.4.4","7.1.4.5","7.2.4.5","7.2.4.6","7.2.4.7","7.3.1.2","7.3.2.3","7.3.2.4","7.3.3.3","7.3.3.4"]
        hashAAA = ["7.1.2.6","7.1.2.7","7.1.2.8","7.1.2.9","7.1.4.6","7.1.4.7","7.1.4.8","7.1.4.9","7.2.1.3","7.2.2.3","7.2.2.4","7.2.2.5","7.2.3.2","7.2.4.8","7.2.4.9","7.2.4.10","7.3.1.3","7.3.1.4","7.3.1.5","7.3.1.6","7.3.2.5","7.3.3.5","7.3.3.6"]
        if level_flag == "A":
            datas = hashA
        elif level_flag == "AA" or level_flag is None:
            datas = hashA + hashAA
        elif level_flag == "AAA":
            datas = hashA + hashAA + hashAAA
        with open(self.guideline_datas_file, "w") as f:
            strbody = '\n'.join(datas)
            print(strbody)
            f.write(strbody)

    def clear_content(self, del_filename):
        with open(del_filename, "w") as f:
            pass
        return


params = argparse.ArgumentParser(usage='%(prog)s [arg1]')
params.add_argument('arg1', help='input the operationCD')
params.add_argument('-o', help='if you need filetering by option, input option')
args = params.parse_args()
operationCD = args.arg1
optionFlag = args.o
app = DataFileUtil(operationCD)

if operationCD == "reset-guideline-datas":
    app.reset_guideline_datas(optionFlag)
elif operationCD == "clear-content":
    if optionFlag is None:
        print("-o オプションでクリアするファイル名を指定してください!")
        exit()
    else:
        app.clear_content(optionFlag)
else:
    pass


    