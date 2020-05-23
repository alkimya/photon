from mimetypes import guess_type
from os import listdir, makedirs
from os.path import splitext, exists, isdir, join
from shutil import copy, move

from PIL.Image import open


def get_date(img):
    """Function to get exif date and time from an image"""
    exif = img.getexif()
    date = exif.get(306)
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
    name = get_date(open(img))
    print(name)
    if name is not None:
        name = name + ext
        return copy(img, name)


def create_tree(file, dir):
    """Create the tree structure of folders of images"""
    try:
        if file is not None:
            print(file)
            dir = dir + '/' + file[0:4] + '/' + file[4:6] + '/' + file[6:8]
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


def copy_photos(source=".", dest="."):
    """Copy all images from a directory tree dir to a destination dest"""
    if isdir(source):  # if this is a directory,
        for child in listdir(source):
            # compose full path to child
            child = join(source, child)
            if isdir(child):
                copy_photos(child, dest)
            else:
                if guess_type(child)[0] is not None \
                        and (guess_type(child)[0].split('/')[0] == 'image'):
                    print(child)
                    new = rename(child)
                    create_tree(new, dest)

