"""Check "if show red rectangles" argument is correct"""

# python libs
import sys

# internal libs
from Show_Images_Differences.help import help_tip

# same lib
# same lib
from Show_Images_Differences.check_argv_correctness.helpers.errors import ERRORS_MESSAGES


def check_show_differences(argv_):
    """Check if "show red rectangles" argument is correct"""

    mode = argv_[3]

    if len(argv_) >= 5:
        if mode in ARGV["show"]:

            is_show_differences = False

            if check_is_check_show_differences(argv_[5]):
                is_show_differences = True
            elif check_is_check_show_differences(argv_[6]):
                is_show_differences = True
            elif check_is_check_show_differences(argv_[7]):
                is_show_differences = True

            if not is_show_differences:
                sys.exit("There is no width value")

        elif mode in ARGV["save"]:

            is_show_differences = False

            if argv_[6].isnumeric():
                is_show_differences = True
                check_legal_value(argv_[6])
            elif argv_[7].isnumeric():
                is_show_differences = True
                check_legal_value(argv_[7])
            elif argv_[8].isnumeric():
                is_show_differences = True
                check_legal_value(argv_[8])

            if not is_show_differences:
                sys.exit("There is no width value")


"""Return bool, check optional argument if on images there will be red rectangles on images"""
ARGV["show differences red rectangles"]


def check_is_check_show_differences(argument):
    return argument in ARGV["show differences red rectangles"]

#    if not check_show_differences_argv(argv_):
#        sys.exit(f'{ERRORS_MESSAGES["invalid show differences"]}\n'
#                 f"{help_tip()}")
