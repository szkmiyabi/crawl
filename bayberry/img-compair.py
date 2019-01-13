import sys
import os
import re
from PIL import Image
from glob import glob
import argparse
import textwrap

class ImageUtil:

    def __init__(self, vect, folder, save_name):
        self.vect = vect
        self.folder = folder
        self.save_name = save_name

    def exec(self):
        canvas_size_tpl = None
        if self.vect == "horizontal":
            canvas_size_tpl = self.get_canvas_size_horizontal()
        elif self.vect == "vertical":
            canvas_size_tpl = self.get_canvas_size_vertical()
        stitched_image = Image.new("RGB", canvas_size_tpl)
        cnt = 0
        if self.vect == "horizontal":
            cnt_width = 0
            for path in glob(os.path.join(self.folder, "*.*")):
                im = Image.open(path)
                if cnt > 0:
                    cnt_width += im.size[0]
                stitched_image.paste(im, (cnt_width, 0))
                cnt += 1
        elif self.vect == "vertical":
            cnt_height = 0
            for path in glob(os.path.join(self.folder, "*.*")):
                im = Image.open(path)
                if cnt > 0:
                    cnt_height += im.size[1]
                stitched_image.paste(im, (0, cnt_height))
                cnt += 1
        stitched_image.save(self.save_name + ".png")

    def get_canvas_size_horizontal(self):
        total_width = 0
        total_height = self.get_max_height()
        for path in glob(os.path.join(self.folder, "*.*")):
            im = Image.open(path)
            tpl = im.size
            total_width += tpl[0]
        return (total_width, total_height)

    def get_canvas_size_vertical(self):
        total_width = self.get_max_width()
        total_height = 0
        for path in glob(os.path.join(self.folder, "*.*")):
            im = Image.open(path)
            tpl = im.size
            total_height += tpl[1]
        return (total_width, total_height)

    def get_max_width(self):
        width = 0
        for path in glob(os.path.join(self.folder, "*.*")):
            try:
                im = Image.open(path)
                tpl = im.size
                tmpwith = tpl[0]
                if width < tmpwith:
                    width = tmpwith
            except:
                pass
        return width
    
    def get_max_height(self):
        height = 0
        for path in glob(os.path.join(self.folder, "*.*")):
            try:
                im = Image.open(path)
                tpl = im.size
                tmpheight = tpl[1]
                if height < tmpheight:
                    height = tmpheight
            except:
                pass
        return tmpheight

params = argparse.ArgumentParser(
    usage='%(prog)s [arg1] [arg2] [arg3]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''
        note:
          arg1 >> 結合する方向 (hotizontal, vertical)
          arg2 >> 対象画像保存先フォルダ
          arg3 >> 結合画像の保存名(拡張子なし)
    ''')
)
params.add_argument('arg1', help='input the Vector')
params.add_argument('arg2', help='input the Folder Name')
params.add_argument('arg3', help='input the Save as File Name')
args = params.parse_args()
vect = args.arg1
folder = args.arg2
save_name = args.arg3

app = ImageUtil(vect, folder, save_name)
app.exec()