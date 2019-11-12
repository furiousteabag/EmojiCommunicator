"""
Set of methods in this class exist for
preparing an image with text on it
written with emojies and faces.

Typical usage example:

    # Writing word "LOVE" with emojies.
    text = "LOVE"
    emoji_list = ["../support_files/emoji/kiss_kissu.png",
                  "../support_files/emoji/kiss_kissu_love_love_loving.png",
                  "../support_files/emoji/kiss_whistle.png",
                  "../support_files/emoji/love_loveu_beautiful_lovely_sexy_attractive_sweetheart_likable_cute_lovable_sweet.png",
                  "../support_files/emoji/loveu_love_arrow_loving_smitten_heart.png",
                  "../support_files/emoji/love_beat_loveu_loving_beating_vibrating_lovely_heart.png",]
    out = write_text_with_emojies(text=text,
                                  emoji_list=emoji_list,
                                  output_dir="../output/")

    # Writing word "HEY" with faces.
    text = "HEY"
    pictures_to_write_missing_letters_with_path = "../support_files/pictures_to_write_letters/"
    out = write_text_with_faces(text=text,
                                pictures_to_write_missing_letters_with_path=pictures_to_write_missing_letters_with_path,
                                output_dir="../output/")
"""


from PIL import ImageFont, ImageDraw, Image, ImageOps

import face_recognition
import numpy as np
import random

import os


"""
Generating pictures.
"""


def write_text_with_squares(phrase,
                            width,
                            height,
                            back_ground_color,
                            margin,
                            font_path,
                            font_size,
                            font_color):
    """Drawing given text with given params.

    Args:
        phrase (int): What text to draw.

    Returns:
        image, font_size.
    """
    image = Image.new("RGBA", (width, height), back_ground_color)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(margin, phrase, font=font, fill=font_color)

    return image, font_size


def write_text_with_squares_not_dependent(phrase,
                                          height=1000,
                                          back_ground_color=(0, 0, 0, 0),
                                          font_color=(0, 0, 0),
                                          font_path="../support_files/fonts/EnhancedDotDigital7-XyLK.ttf"):
    """Shell for write_text_with_squares method.
    """

    width = int(height*2)
    font_size = int(3000/len(phrase))
    margin = (int(width/font_size)*25, int(height/font_size)*150)

    return write_text_with_squares(phrase=phrase,
                                   height=height,
                                   width=width,
                                   back_ground_color=back_ground_color,
                                   font_color=font_color,
                                   font_size=font_size,
                                   margin=margin,
                                   font_path=font_path)


def prepare_emoji_list(emoji_list,
                       font_size):
    """Preparing emojies to be put on picture.
    """

    return list(map(lambda x: x.convert("RGBA").resize((int(font_size/10), int(font_size/10))), emoji_list))


def fill_text_with_emojies(emoji_list,
                           image,
                           back_ground_color=(0, 0, 0, 0)):
    """Filling every pixel which color in not back_ground_color with random emoji.
    """

    image = squeeze_squares_into_pixels(image)

    out = Image.new('RGBA', image.size, back_ground_color)
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) != back_ground_color:
                random_num = random.randint(0, len(emoji_list)-1)
                img_to_paste = emoji_list[random_num]
                out.paste(img_to_paste, (x, y), mask=img_to_paste)

    return out


def write_text_with_emojies(text,
                            emoji_list,
                            output_dir,
                            i=0):
    """Writing given text with given emojies, saving them.
    """

    image, font_size = write_text_with_squares_not_dependent(text)

    emoji_list = list(map(lambda x: Image.open(x), emoji_list))
    emoji_list = prepare_emoji_list(emoji_list, font_size)
    out = fill_text_with_emojies(emoji_list, image)

    out.save(output_dir+str(i)+text+".png", "PNG")

    return out


def write_text_with_faces(text,
                          pictures_to_write_missing_letters_with_path,
                          output_dir,
                          i=0):
    """Writing given text with given faces, saving them.
    """

    pictures_paths_list = list(map(lambda x: pictures_to_write_missing_letters_with_path + x,
                                   os.listdir(pictures_to_write_missing_letters_with_path)))
    pictures_paths_list = list(map(lambda x: crop_face(Image.open(x)), pictures_paths_list))
    pictures_paths_list = list(map(lambda x: make_circled_image(x), pictures_paths_list))

    image, font_size = write_text_with_squares_not_dependent(text)
    pictures_paths_list = prepare_emoji_list(pictures_paths_list, font_size)

    out = fill_text_with_emojies(pictures_paths_list, image)
    out.save(output_dir+str(i)+text+".png", "PNG")

    return out


"""
Cropping and circling face.
"""


def crop_face(img):
    """Returns face from image.
    """

    img_array = np.array(img)
    face_locations = face_recognition.face_locations(img_array)

    x = face_locations[0][3]
    y = face_locations[0][0]
    max_x = face_locations[0][1]
    max_y = face_locations[0][2]

    cut = img.crop((x, y, max_x, max_y))

    return cut


def make_circled_image(img):
    """Making image circled.
    """

    im = img.resize((120, 120))
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output


"""
Writing text with set of pixels.
"""


def square_side_length(image,
                       back_ground_color=(0, 0, 0, 0)):
    """Square side length on picture with squares.

    Args:
        image: Picture with squares on it.
               Squares are similar to each other.
    """
    width, height = image.size
    lengthes = []
    for h in range(height):
        counter = 0
        for w in range(width):
            pixel_color = image.getpixel((w, h))
            if (pixel_color != back_ground_color):
                counter += 1
        if (len(set(lengthes)) < 3):
            lengthes.append(counter)
    return len(list(filter(lambda x: x != 0, lengthes[:-1])))


def squeeze_squares_into_pixels(image,
                                back_ground_color=(0, 0, 0, 0)):
    """Squeezing squares on image into 1 top left pixel.

    Args:
        image: Picture with squares on it.
               Squares are similar to each other.
    """
    width, height = image.size
    side_length = square_side_length(image)
    for w in range(width):
        for h in range(height):
            pixel_color = image.getpixel((w, h))
            if pixel_color != back_ground_color:
                for w_black in range(w, w + side_length):
                    for h_black in range(h, h + side_length):
                        if (w_black != w or h_black != h):
                            image.putpixel((w_black, h_black), back_ground_color)
    return image
