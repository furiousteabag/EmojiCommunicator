"""
This module contains methods collecting all program,
which includes tokenizing input text, make image from
every tokenized word and collect them into .gif.

Typical usage example:

    text = "I'll kill you if you don't get the phone"
    generate_gif(text)
"""


from PIL import Image

from tokenization import get_kphrases, get_emoji
from text_visualization import write_text_with_emojies, write_text_with_faces

import os
import shutil


def generate_gif(text="Sweetheart, I miss you so much",
                 pictures_to_write_missing_letters_with_path="../support_files/pictures_to_write_letters/",
                 output_dir="../output/",
                 emoji_dir="../support_files/emoji/"):
    """Generating .gif from given text.
    """

    clear_dir(output_dir)

    word_list = get_kphrases(text)
    word_list = list(map(lambda x: x.upper(), word_list))

    print("Main words: {}".format(word_list))

    # Adding pictures that will be used for gif.
    for i in range(len(word_list)):

        emoji_list = get_emoji(word_list[i], emoji_dir)

        if emoji_list == []:
            write_text_with_faces(text=word_list[i],
                                  i=i,
                                  pictures_to_write_missing_letters_with_path=pictures_to_write_missing_letters_with_path,
                                  output_dir=output_dir)
        else:
            write_text_with_emojies(text=word_list[i],
                                    emoji_list=emoji_list,
                                    i=i,
                                    output_dir=output_dir)

    print("Succesfully prepared words for .gif, exported in directory: '{}'.".format(output_dir))

    # Making gif.
    filenames = os.listdir(output_dir)
    filenames = list(map(lambda x: output_dir + x, filenames))
    filenames.sort()

    if filenames != []:
        filenames = list(map(lambda x: gen_frame(x), filenames))
        im1 = filenames[0]
        im1.save(output_dir + 'output.gif', save_all=True,
                 append_images=filenames[1:], loop=0, duration=1500, disposal=2)

    print("Succesfully prepared .gif, exported in directory: '{}'.".format(output_dir))


def clear_dir(dir_path):
    for the_file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def gen_frame(path):
    """Preparing image for a transparent gif.
    """
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im
