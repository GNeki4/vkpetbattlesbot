from io import BytesIO
import os
from PIL import Image
import random
import requests


def distort(file_name, percent=None):
    image = Image.open(file_name)
    image_dimensions = image.width, image.height
    distortion_cmd_command = f"magick {file_name} -liquid-rescale {percent}x{percent}%! -resize {image_dimensions[0]}x{image_dimensions[1]}\! {file_name}"

    os.system(distortion_cmd_command)

    buf = BytesIO()
    buf.name = 'image.jpeg'

    image = Image.open(file_name)
    file_type = "JPEG" if file_name.endswith(".jpg") else "PNG"
    image.save(buf, file_type)

    buf.seek(0)

    return file_name


def do_distortion(url, input_percent):
    switcher = {
        1: '80',
        2: '70',
        3: '60',
        4: '50',
        5: '30'
    }
    r = requests.get(url, allow_redirects=True)
    img_name = f'distorted{random.randint(1, 100)}' + '.jpg'
    open(str(img_name), 'wb').write(r.content)

    output_percent = '80'
    try:
        output_percent = switcher.get(input_percent)
    except:
        pass

    return distort(img_name, output_percent)

