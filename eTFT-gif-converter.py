#!/usr/bin/env python

# VERSION 0.1 - eTFT screens - GIF Converter
# ALEX ARCE | alex.arce@pm.me - DEC.2020

import os, re, glob

import PIL
from PIL import Image

import subprocess
import argparse

# --------------------------------------------------------------------

class AnimationConverter:
    def __init__(self, original_animation, animation_header):
        self.gif = original_animation
        self.anim_header = animation_header

    def get_image_size_total(self, filename):
        img = Image.open(filename)
        total_size = img.width * img.height
        img.close()
        return total_size        

    def get_pixel_data(self, filename, file_descriptor):
        img = Image.open(filename)
        if img.mode in ('RGB', 'LA') or (img.mode == 'P' and 'transparency' in img.info):   
            pixels = list(img.convert('RGB').getdata())
            pixels_len = len(pixels) - 1
            for index, pix in enumerate(pixels):
                rgb565 = (((pix[0] & 0xf8) << 8) + ((pix[1] & 0xfc) << 3) + (pix[2] >> 3))    
                if index == pixels_len:
                    file_descriptor.write('0x{:04X}'.format(rgb565))
                else:
                    file_descriptor.write('0x{:04X}'.format(rgb565))
                    file_descriptor.write(',')
        img.close()

    def generate_frames(self):
        # TODO - REsize gif here??
        # ...

        cmd = ['/usr/bin/convert', '-coalesce', self.gif, 'frame_%d.jpg']
        subprocess.call(cmd, shell=False)

    def get_frames_filelist(self):
        filelist = glob.glob("*.jpg")
        filelist.sort(key=lambda f: int(re.sub('\D', '', f)))
        return filelist

    def generate_header_file(self, filelist):
        if len(filelist) > 0:
            fd =  open(self.anim_header, 'x')
            fd.write("int frames = %d;\n" % len(filelist))

            first_frame = filelist[0]
            img = Image.open(first_frame)
            fd.write("int animation_width = %d;\n" % img.width)
            fd.write("int animation_height = %d;\n" % img.height)
            img.close()
        
            # const unsigned short PROGMEM animation[][6700]=
            total_size = self.get_image_size_total(first_frame)
            fd.write("const unsigned short PROGMEM animation[][%d] = {\n" % total_size)

            current_block = 0
            last_block = len(filelist)
            for filename in filelist:
                fd.write("{")
                #fd.write("DATA_BLOCK_%d" % current_block)
                self.get_pixel_data(filename, fd)
                if current_block < last_block - 1:
                    fd.write("},\n")
                else:
                    fd.write("}\n")
                current_block = current_block + 1
            fd.write("};")
            fd.close()
            return True
        else:
            return False

    def Generate(self):
        self.generate_frames()
        frames = self.get_frames_filelist()
        ret = self.generate_header_file(frames)
        return ret

# --------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    gif_file = args.input
    header_file = args.output 

    # If header exists, delete it. Maybe we can change this behavior...
    if os.path.exists(header_file):
        os.remove(header_file)

    converter = AnimationConverter(gif_file, header_file)
    status = converter.Generate()
    print("[+] Conversion result: %d" % status)

# --------------------------------------------------------------------
    
