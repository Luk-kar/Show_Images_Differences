"""Place to hold program's global const"""


# Python
import os
import sys


# https://stackoverflow.com/questions/22812785/use-endswith-with-multiple-extensions
# must be tuple to provide multiply extensions
LEGAL_EXTENSIONS = tuple(".png")

ARGV = {
    "show differences red rectangles": ["show differences red rectangles", "-sd"],
    "search by ratio": ["--search_by_ratio", "-br"],
    "save": ["--save", "-sv"],
    "show": ["--show", "-sh"],
    "help": ["--help", "-h"],
}

IMAGES_SIZES = {
    "highest scale":  4.0,  # to avoid image distortions
    "lowest scale": 0.5,  # to avoid image distortions
    "biggest dimension": 1080,  # to avoid performance issues
    "smallest dimension": 1,
    "default width": 360,
}

SIMILARITY = {
    "enough": 0.95,  # SSMI value in calculating resemblance, 1 is Max
    # Why so low? Well... this is the lowest value in which matching makes any sense
    "not enough": 0.10
}


def set_app_path():

    # https://stackoverflow.com/a/404750/12490791
    program_name = sys.argv[0]

    if getattr(sys, 'frozen', False) or program_name.endswith("__main__.py"):
        application_path = ""  # relative ./
    elif __file__:
        application_path = f"{program_name}/"
    else:
        raise IOError("no path")

    return application_path
