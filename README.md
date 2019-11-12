# Emoji Communicator
Printing text with letters written with emoji.

This project was done on 09.11 - 10.11 during [PhotoHack](https://hackvn.photolab.me/?utm_source=base_baltick_sea_hack) competition.


# Examples
```
python make_gif.py -t "Sweetheart, I miss you so much"
```
![output](https://user-images.githubusercontent.com/32129186/68718662-ef981980-05ba-11ea-9884-963df6e850fc.gif)

```
python make_gif.py -t "I'll kill you if you don't get the phone"
```
![output](https://user-images.githubusercontent.com/32129186/68718909-b57b4780-05bb-11ea-9de9-b358e405c6d7.gif)

```
python make_gif.py -t "I'm stuck in a traffic jam and will be late, all is lost"
```
![output](https://user-images.githubusercontent.com/32129186/68718855-92e92e80-05bb-11ea-958b-8a34015c3186.gif)

# Usage

To use you have to clone this repo, install requirements, go to scripts folder and launch make_gif.py.

```bash
pip install -r requirements.txt
```
Usage example:

```
python make_gif.py -t "Text that you want to visualize."
```
Script accepts additional parameters:

```
usage: make_gif.py [-h] [-t TEXT] [-p PICTURES] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text that you want to make .gif of.
  -p PICTURES, --pictures PICTURES
                        Path to folder with pictures that will be used for
                        painting letters.
  -o OUTPUT, --output OUTPUT
                        Path to folder that .gif will be saved.
```
