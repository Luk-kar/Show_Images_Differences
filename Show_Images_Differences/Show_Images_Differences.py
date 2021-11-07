"""
NAME

    Show_Images_Differences

DESCRIPTION

    Showing visual differences between images
    ========================================

    Show_Images_Differences is used for developers to show visual differences
    between the app's particular screen and reference created by the app's designer.

    It aims to improve workflow for the programmer and also designer.

    For a programmer this tool available instant check of the screen,
    if it is done according to references.

    For the designer, this tool relieve him/her from the task of constant checking,
    if a particular screen was done according to the reference.

    Of course, it can be used for any other matching images purposes

    This program uses image recognition algorithms from https://opencv.org/

AUTHOR

    Karol Łukaszczyk
    e-mail: lukkarcontact@gmail.com
"""


# Python libs
from cv2 import destroyAllWindows
from datetime import datetime
from os import path

# internal libs
from Show_Images_Differences.check_argv_correctness.check_argv_correctness import check_argv_correctness
from Show_Images_Differences.check_argv_correctness.helpers.check_paths import count_legal_images
from Show_Images_Differences.config.config import ARGV, IMAGES_SIZES
from Show_Images_Differences.config.logger import Logger
from Show_Images_Differences.create_similar_images_list.create_similar_images_list import create_similar_images_list
from Show_Images_Differences.help import help_detailed_usage, user_commanded_line_help
from Show_Images_Differences.modes.save import save
from Show_Images_Differences.modes.show import show
from UI.window_displaying_not_found_images import window_displaying_not_found_images


def Show_Images_Differences(_argv):
    """Parsing sys.argv to invoke in chosen modes: save or show, or to get help"""

    check_argv_correctness(_argv)  # todo

    if user_commanded_line_help(_argv):
        return help_detailed_usage()

    # Init variables
    source_ref_path = _argv[1]
    target_ref_path = _argv[2]
    mode = _argv[3]

    by_ratio = None
    show_differences = None
    width = IMAGES_SIZES["default width"]

    if mode in ARGV["show"]:
        output_path = None

        minimal_number_of_arguments = 4

        by_ratio, show_differences, width = get_optional_args(
            _argv, minimal_number_of_arguments)

    elif mode in ARGV["save"]:
        output_path = _argv[4]

        if len(_argv) > 5:

            if _argv[5] in ARGV["search by ratio"]:
                by_ratio = _argv[5]
            elif len(_argv) > 6 and _argv[6] in ARGV["search by ratio"]:
                by_ratio = _argv[6]
            elif len(_argv) > 7 and _argv[7] in ARGV["search by ratio"]:
                by_ratio = _argv[6]

            if _argv[5] in ARGV["show differences"]:
                show_differences = _argv[5]
            elif len(_argv) > 6 and _argv[6] in ARGV["show differences"]:
                show_differences = _argv[6]
            elif len(_argv) > 7 and _argv[7] in ARGV["show differences"]:
                show_differences = _argv[7]

            if _argv[5].isnumeric():
                width = int(_argv[5])
            elif len(_argv) > 6 and _argv[6].isnumeric() and len(_argv) > 6:
                width = int(_argv[6])
            elif len(_argv) > 7 and _argv[7].isnumeric() and len(_argv) > 7:
                width = int(_argv[7])

    messages_summary = []

    # to use in log errors
    script_run_date = _get_script_run_date()

    similar_list = create_similar_images_list(
        source_ref_path,
        target_ref_path,
        script_run_date,
        output_path,
        by_ratio,
    )

    references_counter = count_found_and_not_found_refs(
        source_ref_path, similar_list)
    messages_summary.append(references_counter)

    if mode in ARGV["save"]:

        saving_counter = save(width, similar_list,
                              by_ratio, show_differences,  _argv, script_run_date)
        messages_summary.append(saving_counter)

    elif mode in ARGV["show"]:

        show(width, similar_list, by_ratio, show_differences, _argv)

        # bug fixing with persisting windows
        destroyAllWindows()

        # write down not founded refs
        show_log = Logger().load_saving_bool()
        if show_log:
            window_displaying_not_found_images(source_ref_path, similar_list)

    else:
        raise ValueError("Error: Invalid mode value\n"
                         f" {mode}")

    # Value used in UI message box
    return stringify_lists(messages_summary)


def get_optional_args(_argv, minimal_number_of_arguments):

    by_ratio, show_differences, width = None, None, IMAGES_SIZES["default width"]

    if len(_argv) > minimal_number_of_arguments:
        by_ratio = get_by_ratio(_argv, minimal_number_of_arguments)

        show_differences = get_mark_differences(
            _argv, minimal_number_of_arguments)

        width = get_width(_argv, minimal_number_of_arguments)

    return by_ratio, show_differences, width


def get_width(_argv, minimal_number_of_arguments):

    width = IMAGES_SIZES["default width"]

    if _argv[minimal_number_of_arguments].isnumeric():
        width = int(_argv[minimal_number_of_arguments])
    elif len(_argv) > minimal_number_of_arguments + 1 and _argv[minimal_number_of_arguments + 1].isnumeric():
        width = int(_argv[minimal_number_of_arguments + 1])
    elif len(_argv) > minimal_number_of_arguments + 2 and _argv[minimal_number_of_arguments + 2].isnumeric():
        width = int(_argv[minimal_number_of_arguments + 2])

    return width


def get_mark_differences(_argv, minimal_number_of_arguments):

    return get_option_modificator(_argv, minimal_number_of_arguments, "show differences")


def get_by_ratio(_argv, minimal_number_of_arguments):

    return get_option_modificator(_argv, minimal_number_of_arguments, "search by ratio")


def get_option_modificator(_argv, minimal_number_of_arguments, modificator):

    option = None

    if _argv[minimal_number_of_arguments] in ARGV[modificator]:
        option = _argv[minimal_number_of_arguments]
    elif len(_argv) > minimal_number_of_arguments + 1 and _argv[minimal_number_of_arguments + 1] in ARGV[modificator]:
        option = _argv[minimal_number_of_arguments + 1]
    elif len(_argv) > minimal_number_of_arguments + 2 and _argv[minimal_number_of_arguments + 2] in ARGV[modificator]:
        option = _argv[minimal_number_of_arguments + 2]

    return option


def count_found_and_not_found_refs(source_ref_path, similar_list):
    """return tuple of two integers"""

    references_counter = dict()

    source_images_number = count_source_images(source_ref_path)
    found_matches = count_matches(similar_list)
    not_found_matches = source_images_number - found_matches

    _check_matches_legal_values(found_matches, not_found_matches)  # Fail fast

    if found_matches > 0:
        references_counter["found matches"] = len(similar_list)

    if not_found_matches > 0:
        references_counter["not found matches"] = not_found_matches

    return references_counter


def count_matches(similar_list):
    """return int"""

    if not None in similar_list:
        found_matches = len(similar_list)
    else:
        found_matches = 0

    return found_matches


def concat_stringified_values_and_keys(_list):
    """return list"""

    strings_list = []

    for k, v in _list.items():
        strings_list.append(f"{k}: {str(v)}")

    return strings_list


def stringify_lists(messages_summary):
    """return concated all dicts elements into one string"""

    messages_list = []
    for message in messages_summary:
        stringify = concat_stringified_values_and_keys(message)
        messages_list += stringify

    messages_string = ""
    for message in messages_list:
        messages_string += f"{message}\n"

    return messages_string


def count_source_images(source_ref_path):
    """path could be single file or URL"""

    if path.isdir(source_ref_path):
        return count_legal_images(source_ref_path)

    return 1


def _check_matches_legal_values(found_matches, not_found_matches):
    """Raise error when any args are not positive int"""

    error = "It can't be negative value"

    if found_matches < 0 or not isinstance(found_matches, int):
        raise ValueError(error)

    if not_found_matches < 0 or not isinstance(found_matches, int):
        raise ValueError(error)


def _get_script_run_date():
    """get the date when Refrence-Judge has been run"""

    datetime_object = datetime.now()
    current_date = datetime_object.strftime("%Y_%m_%d-%H_%M")

    return current_date
