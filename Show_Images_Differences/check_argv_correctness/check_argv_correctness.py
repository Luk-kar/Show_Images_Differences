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
from Show_Images_Differences.check_argv_correctness.helpers.check_width_values import check_width_values
from Show_Images_Differences.check_argv_correctness.helpers.check_show_diffrences import check_show_diffrences


def check_argv_correctness(argv_):  # todo
    """check if all argvs have correct paths, modes and width values"""

    program_name = argv_[0]

    if len(argv_) == 2:
        if check_correctness_help_command(argv_):
            sys.exit(f"Error: invalid 1st argument. Usage: python {program_name} {ARGV['help'][0]} or {ARGV['help'][1]}:\n"
                     f" {argv_[1]}")

    if len(argv_) > 2:
        source_ref_path = _argv[1]  # todo

        if len(argv_) > 3:
            target_ref_path = _argv[2]

        if len(argv_) > 4:
            mode = _argv[3]

        if mode in ARGV["show"]:
            output_path = None

            if len(_argv) > 4:

                if _argv[4] in ARGV["search by ratio"]:
                    by_ratio = _argv[4]
                elif len(_argv) > 5 and _argv[5] in ARGV["search by ratio"]:
                    by_ratio = _argv[5]
                elif len(_argv) > 6 and _argv[6] in ARGV["search by ratio"]:
                    by_ratio = _argv[5]

                if _argv[4] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[4]
                elif len(_argv) > 5 and _argv[5] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[5]
                elif len(_argv) > 6 and _argv[6] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[6]

                if _argv[4].isnumeric():
                    width = int(_argv[4])
                elif len(_argv) > 5 and _argv[5].isnumeric():
                    width = int(_argv[5])
                elif len(_argv) > 6 and _argv[6].isnumeric():
                    width = int(_argv[6])

        elif mode in ARGV["save"]:
            output_path = _argv[4]

            if len(_argv) > 5:

                if _argv[5] in ARGV["search by ratio"]:
                    by_ratio = _argv[5]
                elif len(_argv) > 6 and _argv[6] in ARGV["search by ratio"]:
                    by_ratio = _argv[6]
                elif len(_argv) > 7 and _argv[7] in ARGV["search by ratio"]:
                    by_ratio = _argv[6]

                if _argv[5] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[5]
                elif len(_argv) > 6 and _argv[6] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[6]
                elif len(_argv) > 7 and _argv[7] in ARGV["show differences red rectangles"]:
                    show_differences = _argv[7]

                if _argv[5].isnumeric():
                    width = int(_argv[5])
                elif len(_argv) > 6 and _argv[6].isnumeric() and len(_argv) > 6:
                    width = int(_argv[6])
                elif len(_argv) > 7 and _argv[7].isnumeric() and len(_argv) > 7:
                    width = int(_argv[7])

    elif check_correctness_help_command(argv_):
        sys.exit(f"Error: invalid 1st argument. Usage: python {program_name} {ARGV['help'][0]} or {ARGV['help'][1]}:\n"
                 f" {argv_[1]}")

    # correct number of arguments
    elif check_correctness_number_of_args_mode(argv_):

        check_paths(argv_)

        check_mode(argv_)

        check_width_values(argv_)

        check_show_diffrences(argv_)

    else:
        raise ValueError("Invalid usage of program")


def check_correctness_number_of_args_all_cases(argv_):
    """return bool"""
    return not (check_command_help_len(argv_) or check_correctness_number_of_args_mode(argv_))


def check_correctness_help_command(argv_):
    """return bool"""
    return check_command_help_len(argv_) and not argv_[1] in ARGV["help"]


def check_correctness_number_of_args_mode(argv_):
    """return bool"""
    return len(argv_) >= 4 and len(argv_) <= 8


def check_command_help_len(argv_):
    """return bool"""
    return len(argv_) == 2
