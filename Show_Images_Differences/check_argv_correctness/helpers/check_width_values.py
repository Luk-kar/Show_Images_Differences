"""check if width values are not too big, not too small, numeric"""

# python libs
import sys

# internal libs
from Show_Images_Differences.config.config import ARGV, IMAGES_SIZES
from Show_Images_Differences.check_argv_correctness.helpers.errors import get_error_width_too_high, get_error_width_too_low


def check_width_values(argv_):
    """
    check if width value is lower or equal IMAGES_SIZES["biggest dimension"]
    in save or show mode
    """

    mode = argv_[3]

    if len(argv_) >= 5:
        if mode in ARGV["show"]:

            isWidth = False

            if argv_[5].isnumeric():
                isWidth = True
                check_legal_value(argv_[5])
            elif argv_[6].isnumeric():
                isWidth = True
                check_legal_value(argv_[6])
            elif argv_[7].isnumeric():
                isWidth = True
                check_legal_value(argv_[7])

            if not isWidth:
                sys.exit("There is no width value")

        elif mode in ARGV["save"]:

            isWidth = False

            if argv_[6].isnumeric():
                isWidth = True
                check_legal_value(argv_[6])
            elif argv_[7].isnumeric():
                isWidth = True
                check_legal_value(argv_[7])
            elif argv_[8].isnumeric():
                isWidth = True
                check_legal_value(argv_[8])

            if not isWidth:
                sys.exit("There is no width value")


def check_legal_value(_width):
    """check if width value is lower or equal IMAGES_SIZES["biggest dimension"]"""

    width = int(_width)

    # check if value is too high
    if width > IMAGES_SIZES["biggest dimension"]:
        sys.exit(get_error_width_too_high(width))
    elif width < IMAGES_SIZES["smallest dimension"]:
        sys.exit(get_error_width_too_low(width))
