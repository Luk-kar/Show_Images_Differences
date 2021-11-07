"""common functions for helpers"""


# internal libs
from Show_Images_Differences.config.config import ARGV
from Show_Images_Differences.utils import resize_with_with_aspect_ratio


def resize_all(images, width):
    """Change all image size keeping ratio"""

    for image in images:
        if not image == "Source name":  # This is the only value in dict which is not a image
            resize = resize_with_with_aspect_ratio(images[image], width)
            images[image] = resize

    return images


def check_type_width(width):
    """raise error when it's not string"""

    if not isinstance(width, int):
        raise TypeError(f"Wrong type {type(width)}, it should be int")
