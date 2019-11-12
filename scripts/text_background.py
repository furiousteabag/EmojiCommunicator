"""
Methods to place list of emojies to background of a picture
with random scale and rotation.

Typical usage example:

    images_paths = ["../support_files/emoji/kiss_kissu.png",
                    "../support_files/emoji/kiss_kissu_love_love_loving.png",
                    "../support_files/emoji/kiss_whistle.png",
                    "../support_files/emoji/love_loveu_beautiful_lovely_sexy_attractive_sweetheart_likable_cute_lovable_sweet.png",
                    "../support_files/emoji/loveu_love_arrow_loving_smitten_heart.png",
                    "../support_files/emoji/love_beat_loveu_loving_beating_vibrating_lovely_heart.png",]
    image_path = "../output/0LOVE.png"
    num_of_images = 5

    result_image = put_images(images_paths=images_paths,
                              image_path=image_path,
                              num_of_images=num_of_images)
"""


from PIL import Image

import numpy as np
import random


def make_trasparent(image, rate):
    """Making .png image transparent with given rate
    """

    # Load the image and make into Numpy array
    rgba = np.array(image)

    # Make image transparent white anywhere it is transparent
    rgba[rgba[..., -1] == 0] = [255, 255, 255, 0]

    # Make back into PIL Image and save
    rgba_image = Image.fromarray(rgba)

    rgba_image.putalpha(rate)

    rgba_image = rgba_image.convert("RGBA")
    datas = rgba_image.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    rgba_image.putdata(newData)

    return rgba_image


def resizer(image_to_be_put, image):
    """Resizing image_to_be_put so it fits into image.
    """

    r = random.randint(4, 10)
    width_img, height_img = image.size
    width_arrow, height_arrow = image_to_be_put.size
    if (int(width_arrow * r) < int(width_img * 0.5)) or (int(height_arrow * r) < int(height_img * 0.5)):
        new_size = (int(width_arrow * r), int(height_arrow * r))
        print(r)
        image_to_be_put = image_to_be_put.resize(new_size)

        return image_to_be_put
    else:
        resizer(image_to_be_put, image)


def image_maker(image_to_be_put, image):
    """Imposing image_to_be_put to image with random angle and random location.
    """

    resized_arrow = resizer(image_to_be_put, image)
    resized_arrow = make_trasparent(resized_arrow, 100)

    width_img, height_img = image.size

    rangle = random.randint(0, 360)
    new_arrow = resized_arrow.rotate(rangle, expand=True)
    width_new_arrow, height_new_arrow = new_arrow.size
    rx = random.randint(0, height_img - height_new_arrow)
    ry = random.randint(0, width_img - width_new_arrow)

    area = (ry, rx)
    try:
        image.paste(new_arrow, area, new_arrow)
    except Exception as e:
        print(e)

    return image


def put_images_onto_image(images_list, image, num_of_images):
    """Placing images on image.
    """

    for i in range(num_of_images):
        random_num = random.randint(0, len(images_list)-1)
        image_to_be_put = images_list[random_num]
        image = image_maker(image_to_be_put, image)
    return image


def put_images(images_paths, image_path, num_of_images):
    """Shell for put_images_onto_image method.
    """

    images_list = list(map(lambda x: Image.open(x), images_paths))
    images_list = list(map(lambda x: x.resize((60, 60)), images_list))
    image = Image.open(image_path)
    return put_images_onto_image(images_list=images_list,
                                 image=image,
                                 num_of_images=num_of_images)
