"""check if width values are not too big, not too small, numeric"""

# python libs
import sys

# internal libs
from Show_Images_Differences.config.config import ARGV, IMAGES_SIZES
from Show_Images_Differences.check_argv_correctness.helpers.errors import get_error_width_too_high, get_error_width_too_low, ERRORS_MESSAGES
from Show_Images_Differences.help import help_tip


def check_optional_args(argv_):
    """
    check if width value is lower or equal IMAGES_SIZES["biggest dimension"]
    in save or show mode
    """

    mode = argv_[3]

    invalid_optional_arg = []

    if len(argv_) >= 5 and mode in ARGV["show"]:

        if not check_is_optional_argument(argv_[4]):
            invalid_optional_arg.insert(0, argv_[4])
        elif len(argv_) >= 6 and not check_is_optional_argument(argv_[5]):
            invalid_optional_arg.insert(0, argv_[5])
        elif len(argv_) >= 7 and not check_is_optional_argument(argv_[6]):
            invalid_optional_arg.insert(0, argv_[6])

    elif len(argv_) >= 6 and mode in ARGV["save"]:

        if not check_is_optional_argument(argv_[5]):
            invalid_optional_arg.insert(0, argv_[5])
        elif len(argv_) >= 7 and not check_is_optional_argument(argv_[6]):
            invalid_optional_arg.insert(0, argv_[6])
        elif len(argv_) >= 8 and not check_is_optional_argument(argv_[7]):
            invalid_optional_arg.insert(0, argv_[7])

    if invalid_optional_arg:
        for arg in invalid_optional_arg:
            if arg.isnumeric():
                width = arg
                show_error_invalid_width(width)
            else:
                show_error_invalid_option(arg)


def check_is_optional_argument(argument):
    return argument in ARGV["show differences"] or argument in ARGV["search by ratio"] or (argument.isnumeric() and check_legal_value(argument))


def check_legal_value(_width):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimension"]"""

    width = int(_width)

    # check if value is too high
    if width > IMAGES_SIZES["biggest dimension"]:
        return False
    elif width < IMAGES_SIZES["smallest dimension"]:
        return False
    else:
        return True


def show_error_invalid_width(_width):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimension"] and inform client"""

    width = int(_width)

    # check if value is too high
    if width > IMAGES_SIZES["biggest dimension"]:
        sys.exit(get_error_width_too_high(width))
    elif width < IMAGES_SIZES["smallest dimension"]:
        sys.exit(get_error_width_too_low(width))


def show_error_invalid_option(option):
    sys.exit(f"{ERRORS_MESSAGES['invalid arg']}\n"
             + f"{option}\n" +
             f"{help_tip()}")
