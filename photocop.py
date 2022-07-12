from mimetypes import guess_type
from os import listdir
from os import makedirs
from os.path import exists
from os.path import isdir
from os.path import join
from os.path import splitext
from shutil import copy
from shutil import move

from PIL.Image import open


def get_date(img):
    """Function to get exif date and time from an image"""
    exif = img.getexif()
    date = exif.get(306)
    if date is not None:
        date = date.replace(' ', '-').replace(':', '')
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
    if name is not None:
        name = name + ext
        return copy(img, name)


def create_tree(file, rep):
    """Create the tree structure of folders of images"""
    try:
        if file is not None:
            rep = rep + '/' + file[0:4] + '/' + file[0:6] + '/' + file[0:8]
            if not exists(rep):
                makedirs(rep)
                move(file, rep)
            else:
                if not exists(rep + '/' + file):
                    move(file, rep)
                else:
                    print('Already exists!')
    except OSError:
        print('Argh! I could not create the directory!')


def copy_photos(source='.', dest='.'):
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
                    new = rename(child)
                    create_tree(new, dest)


if __name__ == '__main__':
    copy_photos('/home/loc/tmp', '/home/loc/media/images/photos')
