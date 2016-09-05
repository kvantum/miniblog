#!/usr/bin/env python3
# This script allows resizing of a picture, making text and image watermarks.

import os
import sys

from miniblog import app

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFont
except:
    exit("This script requires the PIL module.\nInstall it with 'sudo apt-get \
         install python3-pil' please.")

def resize_image(filename, width, height, outfolder):
    """
    Resizes the image to width x height box size and saves the
    image to outfolder in PNG format.
    :filename: path to the input image
    :width: desired width of output image, an integer number
    :height: desired height of output image, an integer number
    :outfolder: path to the folder for the output image saving
    """
    image = Image.open(filename)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    image_width, image_height = image.size
    if width <= image_width and height <= image_height:
        image_width = width
        image_height = height
    elif width < image_width and height > image_height:
        image_height = (image_height * width) / image_width
        image_width = width
    elif width > image_width and height < image_height:
        image_width = (image_width * height) / image_height
        image_height = height

    layer = Image.new('RGBA', (width, height), (0,0,0,0))
    resized_image = image.resize((int(image_width), int(image_height)))
    position = (int((width - image_width)/2), int((height - image_height)/2))
    layer.paste(resized_image, position)
    new_filename = os.path.split(filename.rsplit('.')[0]+".png")[1]
    layer.save(os.path.join(outfolder, new_filename),'PNG')
    return new_filename

def text_watermark(filename, text, outfolder, angle=25, opacity=0.25):
    """
    Adds a text watermark to the image.
    :filename: path to the input image
    :text: text of a watermark
    :outfolder: path to the folder for the output image saving
    :angle: angle of the watermark text, a float number
    :opacity: watermark opacity, a float number from 0 to 1
    """
    # Font of the text watermark
    font = 'Verdana.ttf'
    # Path to the font. There is a problem of using MS fonts in Linux platforms,
    # so the path to the font should be set manually.
    font_path = "/usr/share/fonts/truetype/msttcorefonts"

    img = Image.open(filename).convert('RGBA')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2

    if sys.platform == "linux" or sys.platform == "linux2":
        font = os.path.join(font_path, font)

    # return watermark TruTypeFont(filename, size, index, encoding)
    wm_font = ImageFont.truetype(font, size)
    # Width and height of the watermark text in pixels
    wm_width, wm_height = wm_font.getsize(text)
    while wm_width + wm_height + 10 < watermark.size[0]:
        size += 2
        wm_font = ImageFont.truetype(font, size)
        wm_width, wm_height = wm_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - wm_width) / 2,
              (watermark.size[1] - wm_height) / 2),
              text, font=wm_font)
    watermark = watermark.rotate(float(angle), Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(os.path.join(outfolder, \
                    filename), 'PNG')

def image_watermark(filename, watermark, outfolder, opacity=0.25):
    """
    Adds a watermark image to the input picture.
    :filename: path to the input image
    :watermark: path to the watermark image
    :outfolder: path to the folder for the output image saving
    :opacity: watermark opacity, a float number from 0 to 1
    """
    watermark = Image.open(watermark)
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    alpha = watermark.split()[3]
    #Reduce the brightness or the 'alpha' band
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    image = Image.open(filename)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    if watermark.size[0] > image.size[0] or watermark.size[1] > image.size[1]:
        watermark = watermark.resize(image.size[0],image.size[1])
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    position = (image.size[0] - watermark.size[0], \
                image.size[1] - watermark.size[1])
    layer.paste(watermark, position)
    Image.composite(layer, image, layer).save(os.path.join(outfolder, \
                                              filename),'PNG')


