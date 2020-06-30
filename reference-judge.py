# python libs
from sys import argv
import os

# external libs
import matplotlib.pyplot as plt
import numpy as np
import cv2

# internal libs
from create_similar_images_list import create_similar_images_list
from compute_image_diffrences import compute_image_diffrences
from app_data import legit_extensions
from utlis import uri_validator


def resize_with_wspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):  # https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display

    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def resize_all(images, width):

    for image in images:
        if not image == "Original_name":  # This is the only value in dict which is not a image
            resize = resize_with_wspect_ratio(images[image], width)
            images[image] = resize

    return images


def format_path(temp_dir, temp_name, index, temp_ext):

    return f"{temp_dir}/{temp_name}-{str(index).zfill(5)}.{temp_ext}"  # example_dir_path/file-0000%.ext


def next_path(path_pattern):  # https://stackoverflow.com/a/47087513/12490791
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """

    temp_dir = os.path.dirname(path_pattern)
    temp_full_name = os.path.basename(path_pattern)
    temp_name, temp_ext = temp_full_name.split('.', 1)  # https://stackoverflow.com/a/6670331/12490791

    i = 1

    # First do an exponential search
    while os.path.exists(format_path(temp_dir, temp_name, i, temp_ext)):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2 # interval midpoint
        a, b = (c, b) if os.path.exists(format_path(temp_dir, temp_name, c, temp_ext)) else (a, c)

    return format_path(temp_dir, temp_name, b, temp_ext).replace("\\", "/")  # .replace("\\", "/") to make path string more consistent


def show_images(images, width):

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Diffrence_RGB"]
    diff = images["Diffrence_Structure"]
    thresh = images["Thresh"]

    # Show images
    cv2.imshow("Original", original)
    cv2.imshow("Modified", modified)
    cv2.imshow("Diffrence_RGB", diff_BGR)
    cv2.imshow("Diffrence_Structure", diff)
    cv2.imshow("Thresh", thresh)


def dir_from_path(path):

    if not os.path.isdir(path):
        path = os.path.dirname(path)
    return path


def dir_exists(path):

    # Get dir path from file path
	path = dir_from_path(path)

	return os.path.exists(path)


def save_images_as_one(images, output_path, width):

    # Resize to default value or custom
    images = resize_all(images, width)

    # Images to display
    original_name = images["Original_name"]
    original = images["Original"]
    modified = images["Modified"]
    diff_BGR = images["Diffrence_RGB"]
    diff = images["Diffrence_Structure"]
    thresh = images["Thresh"]

    # All images have to be RGB, changing grayscale back to RGB
    diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2RGB)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    # Combining all images into one
    numpy_horizontal_concat = np.concatenate([original, modified, diff_BGR, diff, thresh], axis=1)

    # Check if choosed loaction is file like
    ext_file = os.path.splitext(output_path)[1]

    # Check if dir exists
    if not dir_exists(output_path):
        exit(f"Error: Directory doesn't exists: {dir_from_path(output_path)}")

    # When output file has not defined name, only dir
    if not ext_file:
        output_path = os.path.join(output_path, original_name)

    # Check if file already exists, if so, add new one with name incremented by one
    if os.path.exists(output_path):
        output_path = next_path(output_path)

    # User notfication where to search saved image
    print("Saved reference : {} in {}".format(original_name, output_path))

    # Save image into choosed loaction
    cv2.imwrite(output_path, numpy_horizontal_concat)


def get_rid_end_slashes(path):  # It can be used only to the last argument
    # Get rid of "/" or "\", if User mistakenly add it at the end of string
    return path.rstrip('/\\\"\'')


def count_legit_images(directory_path):

    # count all legit images
    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name)) and name.endswith(tuple(legit_extensions))])


def is_empty(directory_path):

    # Init variables
    there_are_files = False

    # check if there is any legit image in directory
    for file_name in os.listdir(directory_path):

        full_path = os.path.join(directory_path, file_name)

        if os.path.isfile(full_path) and file_name.endswith(tuple(legit_extensions)):
            there_are_files = True
            break

    return not there_are_files


def directories_validation(original_reference_directory_path, app_reference_directory_path):

    if app_reference_directory_path == original_reference_directory_path:
        exit('Error: "original references" and "app references" directories are the same')

    if not os.path.exists(original_reference_directory_path):
        exit("Error: Directory with original references does not exist")

    if is_empty(original_reference_directory_path):
        exit("Error: There is no images in Directory with original references")

    if not os.path.exists(app_reference_directory_path):
        exit("Error: Directory with app references does not exist")

    if is_empty(app_reference_directory_path):
        exit("Error: There is no images in Directory with app references")

    if count_legit_images(app_reference_directory_path) < count_legit_images(original_reference_directory_path):
        exit('Error: There are more images in "original references" dir than in "app references" dir')


def check_if_argv_is_correct(argv):

    program_name = argv[0]
    
    # incorrect number of arguments
    if not (len(argv) == 2 or (len(argv) >= 4 and len(argv) <= 6)):
        exit(f"Usage: python {program_name} <orignal_reference_path> <app_reference_path> <--mode> [directory_diffrences_output] [width]\n"  # https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
            "For more information:\n"
            f"python {program_name} --help")

    # correct number of arguments
    if len(argv) >= 4 and len(argv) <= 6:

        original_reference_path = argv[1]
        app_reference_path = argv[2]

        # check if mode is correct
        if not (argv[3] == "--save" or argv[3] == "--show"):
            exit('Error: 3th argument is invalid. It\'s not mode: "--show" or "--save"')
        mode = argv[3]

        # check modes arguments
        if mode == "--save":
            if len(argv) < 5:
                exit("Error: No output path")

            elif len(argv) == 6 and not argv[5].isnumeric():
                exit("Error: 5th, last argument should be numeric")

        elif mode == "--show":
            if len(argv) == 5 and not argv[4].isnumeric():
                exit("Error: 4th, last argument should be numeric")

            elif len(argv) == 6:
                exit("Error: one argument too much")
        else:
            exit("Error: Invalid mode argument")

        # Checking paths arguments
        ext_original = os.path.splitext(original_reference_path)[1]
        # original ref arg is a file
        if ext_original:

            ext_app = os.path.splitext(app_reference_path)[1]
            if ext_app and original_reference_path == app_reference_path:
                # Checking if paths/url are not the same
                exit("Error: Both files have the same path")

        # if orginal images are dir
        else:

            # Checking if many files will be compared to one
            if os.path.isdir(original_reference_path) and (os.path.isfile(app_reference_path) or uri_validator(app_reference_path)):
                exit("Error: Original reference path can't be directory, if app reference is only one file")

            directories_validation(original_reference_path, app_reference_path)



def program_help(argv):

    program_name = argv[0]
    
    if len(argv) == 2 and argv[1] == "--help":
        exit("\n"
            "On desktop:\n"
            " save:\n"
            f"  python {program_name} path_dir path_dir --save path_dir [px]\n"
            f"  python {program_name} path_dir path_dir --save path_file [px]\n"
            f"  python {program_name} path_file path_dir --save path_dir [px]\n"
            f"  python {program_name} path_file path_file --save path_dir [px] *\n"
            f"  python {program_name} path_file path_file --save path_file [px] *\n"
            "\n"
            " show:\n"
            f"  python {program_name} path_dir path_dir --show [px]\n"
            f"  python {program_name} path_file path_dir --show [px]\n"
            f"  python {program_name} path_file path_file --show [px] *\n"
            "\n"
            "HTTPS:\n"
            " save:\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img --save path_dir [px] *\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img --save path_file [px] *\n"
            f"  python {program_name} https/address.com/image.img path_dir --save path_dir [px]\n"
            f"  python {program_name} https/address.com/image.img path_dir --save path_file [px]\n"
            f"  python {program_name} path_file https/address.com/image.img --save path_dir [px] *\n"
            f"  python {program_name} path_file https/address.com/image.img --save path_file [px] *\n"
            "\n"
            " show:\n"
            f"  python {program_name} https/address.com/image.img https/address.com/image.img --show [px] *\n"
            f"  python {program_name} path_file https/address.com/image.img --show [px] *\n"
            f"  python {program_name} https/address.com/image.img path_file --show [px] *\n"
            f"  python {program_name} https/address.com/image.img path_dir --show [px]\n"
            "\n"
            " * images have to be the same size"
            " [px] is optional value of width of each image"
            )
    elif len(argv) == 2:
        exit(f"Error: invalid 1st argument. Avaible usage: python {program_name} --help")


def main():

    check_if_argv_is_correct(argv)
    program_help(argv)

    # Init variables
    original_ref_path = get_rid_end_slashes(argv[1])
    app_ref_path = get_rid_end_slashes(argv[2])
    mode = argv[3]

    similar_list = create_similar_images_list(original_ref_path, app_ref_path)

    if mode == "--save":

        # Optional args
        if len(argv) >= 5:
            output_path = get_rid_end_slashes(argv[4])
        else:
            output_path = None

        if len(argv) == 6:
            width = int(argv[5])  # Input user is width of reference image size
        else:
            width = 360  # Default

        
        # Process all images, save each sequence in choosed director
        for similar_pair in similar_list:

            if not similar_pair == None:

                images = compute_image_diffrences(similar_pair)

                save_images_as_one(images, output_path, width)

    elif mode == "--show":

        # Optional arg
        if len(argv) == 5:
            width = int(argv[4])

        else:
            width = 360  # Default

        # Process all images, show user each sequence one by one
        for similar_pair in similar_list:

            if not similar_pair == None:

                images = compute_image_diffrences(similar_pair)

                show_images(images, width)

                print('NOTE: Press the "0" key, to close opened windows')
                cv2.waitKey(0)

    exit(0)

if __name__ == "__main__":
    main()