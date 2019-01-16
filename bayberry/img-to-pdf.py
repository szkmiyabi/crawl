import sys
import os
from glob import glob
import argparse
import re
import img2pdf
from PIL import Image

class ImageToPdf:

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.output_dir_name = "PDF/"
    
    def del_alpha_channel(self):
        print("pngファイルの下処理をします...")
        for path in glob(os.path.join(self.dir_name, "*.png")):
            print(self.get_filename(path), "を処理しています。")
            im = Image.open(path)
            if im.mode == "RGBA":
                im = im.convert("RGB")
            im.save(path)
    
    def exec(self):
        if not os.path.exists(self.output_dir_name):
            os.makedirs(self.output_dir_name)
        self.del_alpha_channel()
        print("PDF出力を開始します...")
        for path in glob(os.path.join(self.dir_name, "*.png")):
            print(self.get_filename(path), " を処理しています。")
            with open(self.output_dir_name + self.get_pfd_filename(path), "wb") as f:
                f.write(img2pdf.convert(path))

    def get_filename(self, path):
        return os.path.basename(path)
    
    def get_pfd_filename(self, path):
        filename = os.path.basename(path)
        return re.sub(r'\.png', ".pdf", filename)


params = argparse.ArgumentParser(usage='%(prog)s [arg1]')
params.add_argument('arg1', help='input the Image Directory')
args = params.parse_args()
dir_name = args.arg1

app = ImageToPdf(dir_name)
app.exec()