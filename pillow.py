"""dev mode"""
import gi
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Colorspace, Pixbuf
from gi.repository.GLib import Bytes

from PIL import Image, ImageFilter
from PIL.Image import Resampling
from PIL.ExifTags import TAGS

from profile import timing

BLUR = ImageFilter.BLUR
CONTOUR = ImageFilter.CONTOUR
DETAIL = ImageFilter.DETAIL
EDGE_ENHANCE = ImageFilter.EDGE_ENHANCE
EDGE_ENHANCE_MORE = ImageFilter.EDGE_ENHANCE_MORE
EMBOSS = ImageFilter.EMBOSS
FIND_EDGES = ImageFilter.FIND_EDGES
SHARPEN = ImageFilter.SHARPEN
SMOOTH = ImageFilter.SMOOTH
SMOOTH_MORE = ImageFilter.SMOOTH_MORE
MinFilter = ImageFilter.MinFilter
MaxFilter = ImageFilter.MaxFilter
MedianFilter = ImageFilter.MedianFilter
UnsharpMask = ImageFilter.UnsharpMask

def to_pil(pix):
    """Convert Gdkpixbuf to PIL image"""
    data = pix.get_pixels()
    props = pix.props
    width, height, stride = props.width, props.height, props.rowstride
    mode = "RGB"
    if props.has_alpha:
        mode = "RGBA"
    pil = Image.frombytes(mode, (width, height), data, "raw", mode, stride)
    return pil


def to_pix(pil):
    """Convert Pillow image to GdkPixbuf"""
    data = pil.tobytes()
    width, height = pil.size
    data = Bytes.new(data)
    pix = Pixbuf.new_from_bytes(data, Colorspace.RGB, False, 8, width, height, width * 3)
    return pix


def imread(url):
    """Open a file from url as a Pillow image"""
    return Image.open(url)


def has_exif(url):
    """Test if an image has exif metadata"""
    return True if len(imread(url).getexif()) != 0 else False


def exif_table(url):
    """Return exif metadata of an image"""
    image = imread(url)
    out = ''
    for k, v in image.getexif().items():
        out = out + str(TAGS.get(k)) + ' : ' + str(v) + '\n'
    return out


def magic_enhance(pil):
    """Fast enhancer filter"""
    pil = pil.filter(EDGE_ENHANCE).filter(SMOOTH)
    return pil


def simple_filter(pil, fil):
    """Apply predefined filter """
    pil = pil.filter(fil)
    return pil


def test(pil):
    """Filter test to check"""
    pil = pil.filter(MaxFilter)
    return pil


@timing
def rotate(pil, angle):
    """Rotate an image by an angle (anti-clockwise)"""
    return pil.rotate(angle)


@timing
def resize(pil, size):
    """Resize an image"""
    return pil.resize(size, resample=Resampling.BILINEAR)

def get_date(pil):
    """Function to get exif date and time from an image"""
    exif = pil.getexif()
    date = exif.get(306)
    if date is not None:
        date = date.replace(' ', '-').replace(':', '')
    return date