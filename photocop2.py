from os import listdir, makedirs
from os.path import splitext, exists, isdir, join, getmtime
from shutil import copy, move
from mimetypes import guess_type
from datetime import datetime
from PIL.Image import open


def get_date(img):
    """Function to get exif date and time from an image"""
    if img is not None:
        date = str(datetime.fromtimestamp(getmtime(img)))
        # date = date[0:16]
    # exif = img.getexif()
    # date = exif.get(306)
    if date is not None:
        date = date.replace(" ", "-").replace(":", "")
    return date


def resize(img, pct):
    """Resize an image with pct as %"""
    size = (img.width * pct // 100, img.height * pct // 100)
    img = img.resize(size)
    return img


def rename(img):
    """Rename an image old with new name"""
    ext = splitext(img)[1].lower()
    name = get_date(img)
    if name is not None:
        name = name + ext
        return copy(img, name)


def create_tree(file, dir):
    """Create the tree structure of folders of images""" 
    try:
        if file is not None:
            print(file)
            dir = dir + '/' + file[0:4] + '/' + file[5:7] + '/' + file[8:10]
            if not exists(dir):
                makedirs(dir)
                move(file, dir)
            else:
                if not exists(dir + '/' + file):
                    move(file, dir)
                else:
                    print('Already exists!')
    except OSError:
        print('Argh! I could not create the directory!')


def copy_photos(dir=".", dest="."):
    """Copy all images from a directory tree dir to a destination dest"""
    if isdir(dir):  # if this is a directory,
        for child in listdir(dir):
            # compose full path to child
            child = join(dir, child)
            if isdir(child):
                copy_photos(child, dest)
            else:
                if guess_type(child)[0] is not None and (guess_type(child)[0].split('/')[0] == 'image'):
                    new = rename(child)
                    create_tree(new, dest)


if __name__ == "__main__":
    copy_photos('/home/loc/tmp', '/home/loc/images/photos')
