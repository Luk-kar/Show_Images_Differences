"""
This module is responsible for checking if program arguments are correct
"""


# python lib
import sys

# internal libs
from Show_Images_Differences.config.config import ARGV
from Show_Images_Differences.help import help_command_line, help_tip

# same lib
from Show_Images_Differences.check_argv_correctness.helpers.check_mode import check_mode
from Show_Images_Differences.check_argv_correctness.helpers.check_paths import check_paths
from Show_Images_Differences.check_argv_correctness.helpers.check_optional_args import check_optional_args


def check_argv_correctness(argv_):
    """check if all argvs have correct paths, modes and width values"""

    program_name = argv_[0]

    # correct number of arguments
    if check_correctness_number_of_args_mode(argv_):

        if len(argv_) == 2:
            if check_correctness_help_command(argv_):
                sys.exit(f"Error: invalid 1st argument. Usage: python {program_name} {ARGV['help'][0]} or {ARGV['help'][1]}:\n"
                         f" {argv_[1]}")

        elif len(argv_) > 2:

            check_paths(argv_)

            check_mode(argv_)

            check_optional_args(argv_)

    else:
        get_error_invalid_argument()


def get_error_invalid_argument():
    sys.exit(f"{help_command_line()}\n"
             f"{help_tip()}")


def check_correctness_help_command(argv_):
    """return bool"""
    return check_command_help_len(argv_) and not argv_[1] in ARGV["help"]


def check_correctness_number_of_args_mode(argv_):
    """return bool"""
    return len(argv_) >= 4 and len(argv_) <= 7


def check_command_help_len(argv_):
    """return bool"""
    return len(argv_) == 2
