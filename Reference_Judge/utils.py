"""
This module are repeating snipsets of functions which are used in many places in application
"""


# python libs
import os
from sys import exit as sys_exit
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

# external libs
import cv2
import numpy as np
# internal libs
from config import ARGV, IMAGES_SIZES


def check_ratio_argv(_argv):
    """Return bool, check optional argument if images are searched by same ratio"""

    # [-1] To avoid checking 3 places at one, this argument is always last
    return bool(_argv[-1] in ARGV["search by ratio"])


# https://stackoverflow.com/a/58126805/12490791
def resize_with_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """Resize input image by width or height keeping proportion to the image"""

    dimension = None
    (h_source, w_source) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        resize = height / float(h_source)
        dimension = (int(w_source * resize), height)
    else:
        resize = width / float(w_source)
        dimension = (width, int(h_source * resize))

    return cv2.resize(image, dimension, interpolation=inter)


def error_check_path_is_empty_string(path):
    """
    Used to fail fast than too late.
    Also to avoid empty string in os path (when path is empty it takes script directory)
    """
    if path == "":
        raise ValueError("Error: variable is empty string")


def dir_from_path(path):
    """If path is file address. Strip file name and retrieve dir directory"""

    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def dir_exists(path):
    """
    Check if directory path exists. Even when path is dir + file.
    It is recommended to use when you want to check
    if directory in path where you want to create new file exists.
    """

    # https://docs.python.org/3/library/pathlib.html
    file_ext = Path(path).suffix

    # Retrieve dir path from file path
    if file_ext:
        path = dir_from_path(path)

    return os.path.isdir(path)


def url_to_image(url):  # https://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
    """
    download the image, convert it to a NumPy array,
    and then read it into OpenCV format
    """

    response = urllib.request.urlopen(url)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def uri_validator(path):  # https://stackoverflow.com/a/38020041/12490791
    """Check if web address is syntacly valid"""

    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc, result.path])
    except:  # todo not sure what type exception is it
        return False


class MakeSizesOfImagesTheSame:
    """
    Resize target image to the same size as source image,
    if ratio between width and height of both images are the same
    """

    def __init__(self, source, target):
        self.w_source, self.h_source, self.w_target, self.h_target = self.take_images_dimensions(
            source, target)

        # ratio have to be same to match images
        self.same_ratio = self.check_if_ratios_are_same()

        # to avoid too big size differences between images and therefore distortions
        self.comparable_sizes = self.check_if_scale_is_similar()

    def check_if_scale_not_too_big(self):
        """images have to have the same ratio and comparable sizes"""

        is_OK = self.same_ratio and self.comparable_sizes

        return is_OK

    # I know it's not elegant but I've done it for performance reasons. self.target -> target
    def give_resized_image(self, target):
        """It returns target image"""
        target = resize_with_with_aspect_ratio(target, self.w_source)

        return target

    def check_if_scale_is_similar(self):
        """return boolean if scale is bigger than 'lowest scale' and smaller than 'highest scale'"""

        compared_ratio = self.w_source/self.w_target

        comparable_sizes = bool(
            IMAGES_SIZES["lowest scale"] <= compared_ratio <= IMAGES_SIZES["highest scale"])

        return comparable_sizes

    def check_if_ratios_are_same(self):
        """return boolean if ratios of the same images are the same"""

        source_ratio = self.w_source/self.h_source
        target_ratio = self.w_target/self.h_target

        same_ratio = (source_ratio == target_ratio)

        return same_ratio

    @staticmethod
    def take_images_dimensions(source, target):
        """get width and height of both images"""

        (h_source, w_source) = source.shape[:2]
        (h_target, w_target) = target.shape[:2]

        return w_source, h_source, w_target, h_target

    def notify_user_about_wrong_scale(self):
        compared_ratio = self.w_source/self.w_target

        if compared_ratio < IMAGES_SIZES["lowest scale"]:
            sys_exit(f"Reference image is size {compared_ratio} times than app image\n"
                     f"min resize value: {IMAGES_SIZES['lowest scale']}"
                     )
        elif compared_ratio > IMAGES_SIZES["highest scale"]:
            sys_exit(f"Reference image is size {compared_ratio} times than app image\n"
                     f"max value: {IMAGES_SIZES['highest scale']}"
                     )
        else:
            raise ValueError("invoked function for wrong ratio values")
