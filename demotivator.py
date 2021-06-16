import random
import PIL
from PIL import Image, ImageDraw, ImageFont
import requests

TEMPLATE_FILENAME = 'template.jpg'
PHRASES_FILENAME = 'phrases.txt'
IMAGES_DIRECTORY = 'images'
EXTENSIONS = ['.jpg', '.png']

UPPER_FONT = 'times.ttf'
UPPER_SIZE = 45
UPPER_FONT_Y = 390
LOWER_FONT = 'arialbd.ttf'
LOWER_SIZE = 14
LOWER_FONT_Y = 450

TEMPLATE_WIDTH = 574
TEMPLATE_HEIGHT = 522
TEMPLATE_COORDS = (75, 45, 499, 373)
PADDING = 10


def is_valid_extension(filename):
    for extension in EXTENSIONS:
        if filename.endswith(extension):
            return True
    return False


def draw_x_axis_centered_text(image, text, font, size, pos_y):
    draw = ImageDraw.Draw(image)
    textFont = ImageFont.truetype(font, size)
    textWidth = textFont.getsize(text)[0]

    while textWidth >= TEMPLATE_WIDTH - PADDING * 2:
        textFont = ImageFont.truetype(font, size)
        textWidth = textFont.getsize(text)[0]
        size -= 1

    draw.text(((TEMPLATE_WIDTH - textWidth) / 2, pos_y), text, font = textFont)


def get_size_from_area(area):
    return (area[2] - area[0], area[3] - area[1])


def make_image(source_image_name, first_phrase, second_phrase):
    frame = PIL.Image.open(TEMPLATE_FILENAME)
    demot = PIL.Image.open(source_image_name)
    demot = demot.resize(get_size_from_area(TEMPLATE_COORDS), PIL.Image.ANTIALIAS)
    frame.paste(demot, TEMPLATE_COORDS)

    draw_x_axis_centered_text(frame, first_phrase,
                              UPPER_FONT, UPPER_SIZE,
                              UPPER_FONT_Y)
    draw_x_axis_centered_text(frame, second_phrase,
                              LOWER_FONT, LOWER_SIZE,
                              LOWER_FONT_Y)

    frame = frame.convert('RGB')
    frame.save(source_image_name)
    return source_image_name
    # frame.show()


def get_demotivator(url, first_phrase, second_phrase):
    r = requests.get(url, allow_redirects=True)
    img_name = f'demotivator{random.randint(1, 100)}' + '.jpg'
    open(str(img_name), 'wb').write(r.content)

    return make_image(img_name, first_phrase, second_phrase)
