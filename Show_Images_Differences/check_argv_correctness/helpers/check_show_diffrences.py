"""Check "if show red rectangles" argument is correct"""

# python libs
import sys

# internal libs
from Show_Images_Differences.help import help_tip
from Show_Images_Differences.utils import check_show_differences_argv

# same lib
# same lib
from Show_Images_Differences.check_argv_correctness.helpers.errors import ERRORS_MESSAGES


def check_show_differences(argv_):
    """Check if "show red rectangles" argument is correct"""

    if not check_show_differences_argv(argv_):
        sys.exit(f'{ERRORS_MESSAGES["invalid show differences"]}\n'
                 f"{help_tip()}")
