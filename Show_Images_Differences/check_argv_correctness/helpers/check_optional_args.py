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

        minimal_argument_number = 4

        check_iteration_through_last_args(argv_, invalid_optional_arg,
                                          minimal_argument_number)

    elif len(argv_) >= 6 and mode in ARGV["save"]:

        minimal_argument_number = 5

        check_iteration_through_last_args(argv_, invalid_optional_arg,
                                          minimal_argument_number)

    if invalid_optional_arg:
        for arg in invalid_optional_arg:
            if arg.isnumeric():
                width = arg
                show_error_invalid_width(width)
            else:
                show_error_invalid_option(arg)


def check_iteration_through_last_args(argv_, invalid_optional_arg, minimal_argument_number):

    for x in range(minimal_argument_number, minimal_argument_number + 3):
        if len(argv_) >= x + 1 and not check_is_optional_argument(argv_[x]):
            invalid_optional_arg.insert(0, argv_[x])


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
