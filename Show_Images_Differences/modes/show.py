"""show matched images to user, each one in separate window"""


# external libs
import cv2

# internal libs
from Show_Images_Differences.compute_image_differences import compute_image_differences

# same module
from Show_Images_Differences.modes.utils import (
    check_correctness_optional_argvs,
    check_width_argv_exists,
    check_type_width,
    retrieve_argv_width, resize_all
)


def show(width, similar_list, by_ratio, show_differences, _argv):
    """show matched images"""

    # Optional args
    if len(_argv) >= 15:  # todo
        check_correctness_optional_argvs(_argv, 6)
        if check_width_argv_exists(_argv, 6):
            width = retrieve_argv_width(_argv, 6)

    check_type_width(width)  # fail fast

    # Process all images, show user each sequence one by one
    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(
                similar_pair, by_ratio, show_differences)

            show_images(width, images)

            print('NOTE: Press the "0" key, to close opened windows')
            cv2.waitKey(0)


def show_images(width, images):
    """show user differences between source and target and images"""

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images
    source = images["Source"]
    target = images["Target"]
    diff_BGR = images["Difference RGB"]
    diff = images["Difference Structure"]
    thresh = images["Thresh"]

    # Show images, please remember that dictionary is not ordered
    cv2.imshow("Source", source)
    cv2.imshow("Target", target)
    cv2.imshow("Difference RGB", diff_BGR)
    cv2.imshow("Difference Structure", diff)
    cv2.imshow("Thresh", thresh)
