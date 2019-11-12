from generate_gif import generate_gif
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str,
                        help="Text that you want to make .gif of.",
                        default="Sweetheart, I miss you so much")
    parser.add_argument("-p", "--pictures", type=str,
                        help="Path to folder with pictures that will be used for painting letters.",
                        default="../support_files/pictures_to_write_letters/")
    parser.add_argument("-o", "--output", type=str,
                        help="Path to folder that .gif will be saved.",
                        default="../output/")
    args = parser.parse_args()
    generate_gif(text=args.text,
                 pictures_to_write_missing_letters_with_path=args.pictures,
                 output_dir=args.output)
