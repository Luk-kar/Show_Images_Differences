"""save matched images in chosen directory"""


# Python libs
from collections import defaultdict
import os

# external libs
import cv2
import numpy as np

# internal libs
from Show_Images_Differences.add_text_to_image.add_text_to_image import add_text_to_image, is_bigger_than
from Show_Images_Differences.compute_image_differences import compute_image_differences
from Show_Images_Differences.config.logger import Logger, write_in_log

# same module
from Show_Images_Differences.modes.utils import (
    check_type_width,
    resize_all
)


def save(width, similar_list, by_ratio, show_differences, _argv, script_run_date):
    """save matched images in chosen directory"""

    if len(_argv) >= 5:
        output_path = _argv[4]
    else:
        output_path = None

    check_type_width(width)  # fail fast

    # Process all images, save each sequence in chosen director

    # https://stackoverflow.com/a/1602964/12490791
    saving_counter = defaultdict(int)

    for similar_pair in similar_list:

        if not similar_pair is None:

            images = compute_image_differences(
                similar_pair, by_ratio, show_differences)

            saved = save_images_as_one(
                images,
                output_path,
                width,
                script_run_date
            )

            if saved:
                saving_counter["saved matches"] += 1
            else:
                saving_counter["not saved matches"] += 1

    return saving_counter


def save_images_as_one(images, output_path, width, script_run_date):
    """save source and target images with images showing differences in one image"""

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images to display
    source_name = images["Source name"]
    source = images["Source"]
    target = images["Target"]
    diff_BGR = images["Difference RGB"]
    diff = images["Difference Structure"]
    thresh = images["Thresh"]

    # All images have to be RGB, changing grayscale back to RGB
    diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    # check if canvas is too small to add text
    if is_bigger_than(100, source):

        source = add_text_to_image(source, "Source")
        target = add_text_to_image(target, "Target")
        diff_BGR = add_text_to_image(diff_BGR, "Difference RGB")
        diff = add_text_to_image(diff, "Difference Structure")
        thresh = add_text_to_image(thresh, "Thresh")

    # Combining all images into one NOTE: please remember that that dictionary is not ordered
    numpy_horizontal_concat = np.concatenate(
        [source, target, diff_BGR, diff, thresh], axis=1)

    # Check if chosen location is file like
    ext_file = os.path.splitext(output_path)[1]

    # Define output path
    if not ext_file:
        output_path = os.path.join(output_path, source_name)

    # Check if file already exists, if so, add new one with name incremented by one
    if os.path.exists(output_path):
        output_path = next_path(output_path)

    # Save image into chosen location
    writeStatus = cv2.imwrite(output_path, numpy_horizontal_concat)

    # User notification where to search saved image: https://stackoverflow.com/a/51809038/12490791
    if writeStatus is True:

        print(f"Saved reference:\n  {source_name}\n  {output_path}")
        saved = True

    else:

        print(f"Not saved:\n  {source_name}")
        saved = False

        save_log = Logger().load_saving_bool()
        if save_log:
            write_in_log("[UNSAVED]", output_path, script_run_date)

    return saved


def next_path(path_pattern):  # https://stackoverflow.com/a/47087513/12490791
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-00001.txt
    file-00002.txt
    file-00003.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    temp_dir = os.path.dirname(path_pattern)
    temp_full_name = os.path.basename(path_pattern)
    # https://stackoverflow.com/a/6670331/12490791
    temp_name, temp_ext = temp_full_name.split('.', 1)

    i = 1

    # First do an exponential search
    while os.path.exists(format_path(temp_dir, temp_name, i, temp_ext)):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (first..last] and narrow it down until first + 1 = last
    first, last = (i // 2, i)
    while first + 1 < last:
        mid = (first + last) // 2  # interval midpoint
        first, last = (mid, last) if os.path.exists(format_path(
            temp_dir, temp_name, mid, temp_ext)) else (first, mid)

    # .replace("\\", "/") to make path string more consistent
    return format_path(temp_dir, temp_name, last, temp_ext).replace("\\", "/")


def format_path(temp_dir, temp_name, index, temp_ext):
    """example_dir_path/file-0000%.ext"""

    return f"{temp_dir}/{temp_name}-{str(index).zfill(5)}.{temp_ext}"
