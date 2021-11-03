"""check correctness of mode args and accompanying arguments"""


# Python libs
import sys

# internal libs
from Show_Images_Differences.config.config import ARGV
from Show_Images_Differences.help import help_tip

# same lib
from Show_Images_Differences.check_argv_correctness.helpers.errors import ERRORS_MESSAGES


def check_mode(argv_):
    """Check if images have to be saved or they have be shown"""

    mode = argv_[3]

    # check modes arguments
    if mode in ARGV["save"]:

        check_mode_save(argv_)

    elif not mode in ARGV["show"]:

        sys.exit(f'{ERRORS_MESSAGES["not mode"]}\n'
                 f" {argv_[3]}\n"
                 f"{help_tip()}")

    return mode


def check_mode_save(argv_):
    """check correctness all argv in save mode"""

    # USE ONLY HERE
    def is_output_path(argv_):
        return len(argv_) < 5

    if is_output_path(argv_):
        sys.exit(f"{ERRORS_MESSAGES['no output']}\n"
                 f"{help_tip()}")


def is_5th_by_ratio(argv_):
    """return bool"""
    return argv_[5] in ARGV["search by ratio"]


def is_legal_width(argv_, i):
    """return bool"""
    return argv_[i].isnumeric()
