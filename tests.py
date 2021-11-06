"""App integration test"""


import os
import shutil
import unittest
import sys
from io import StringIO

import cv2

from Show_Images_Differences.help import help_tip, help_command_line
from Show_Images_Differences.config.config import ARGV, LEGAL_EXTENSIONS, IMAGES_SIZES
from Show_Images_Differences.check_argv_correctness.helpers.check_paths import count_legal_images
from Show_Images_Differences.Show_Images_Differences import Show_Images_Differences
from Show_Images_Differences.check_argv_correctness.helpers.errors import (
    ERRORS_MESSAGES,
    get_error_directory_does_not_exists,
    get_error_no_images_in_dir,
    get_error_width_too_high,
    get_error_width_too_low,

)

# https://stackoverflow.com/a/54955094/12490791

os.system("")


class Style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def print_image_show_up_notification():
    print(Style.BLUE + 'NOTE: Press the "0" key, to close opened windows' + Style.RESET)


def _get_app_absolute_dir_path(path):
    """It works only in tests dir"""

    file_dir = os.getcwd()
    return os.path.join(file_dir, path)


def get_program_name():
    """return string"""
    return sys.argv[0]


def make_folder_empty(folder):
    """delete everything except .gitignore"""

    for filename in os.listdir(folder):
        if filename != ".gitignore":
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except OSError as e:
                print('Failed to delete\n  %s\nReason:\n  %s' % (file_path, e))


def check_if_width_is_correct(width, output_folder):
    are_correct = True

    for filename in os.listdir(output_folder):

        file_path = os.path.join(output_folder, filename)

        if os.path.isfile(file_path) and file_path.endswith(LEGAL_EXTENSIONS):

            img = cv2.imread(file_path, 0)
            width_image = img.shape[1]

            if int(width_image / 5) != int(width):
                are_correct = False
                break

    return are_correct


def test_save_mode(self, _argv, number_of_saved):

    # parse to pass in legal_5_times_widths
    if self.width in _argv:
        width = self.width
    else:
        width = self.width_DEFAULT

    # make sure that folder is empty
    if self.refresh_folder:
        make_folder_empty(self.output_dir)

    # run module
    Show_Images_Differences(_argv)

    # check conditions
    number_of_created_files = count_legal_images(self.output_dir)
    legal_5_times_widths = check_if_width_is_correct(
        width, self.output_dir)

    # refresh folder
    if self.refresh_folder:
        make_folder_empty(self.output_dir)

    with self.subTest():
        self.assertEqual(number_of_created_files,
                         number_of_saved, f"Should be {number_of_saved}")

    with self.subTest():
        self.assertTrue(legal_5_times_widths,
                        "Should be 5 more than width input")


def test_show_mode(self, _argv, number_of_showed):

    print_image_show_up_notification()

    with Capturing() as output:

        Show_Images_Differences(_argv)

    output_occurrence = output.count(
        'NOTE: Press the "0" key, to close opened windows')

    self.assertEqual(output_occurrence, number_of_showed,
                     f"Should be {number_of_showed}")


def test_FAIL_argv(self, _argv, error_message):

    with self.assertRaises(SystemExit) as cm:
        # run module
        Show_Images_Differences(_argv)

    self.assertEqual(cm.exception.code, error_message)


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


program_name = get_program_name()

images_path = "data\\images"
test_paths = {
    "custom name": "new name.png",
    "source dir": images_path + "\\original",
    "target dir": images_path + "\\modified",
    "output dir": images_path + "\\output",
    "source file": "screen002.png",
    "target file": "screen002.png",
    "http source": "https://raw.githubusercontent.com/Luk-kar/Show_Images_Differences/master/data/images/http/screen003.png",
    "http target": "https://raw.githubusercontent.com/Luk-kar/Show_Images_Differences/master/data/images/http/screen003_other.png",
    "source file http": "screen003.png",
    "target file http": "screen003.png",
    "by ratio": ARGV["search by ratio"][0],
    "random": "pizza time!"
}


class TestReferenceJudge(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestReferenceJudge, self).__init__(*args, **kwargs)

        self.source_dir = _get_app_absolute_dir_path(test_paths["source dir"])
        self.target_dir = _get_app_absolute_dir_path(test_paths["target dir"])
        self.output_dir = _get_app_absolute_dir_path(test_paths["output dir"])

        # make sure that folder is empty to run test correctly
        make_folder_empty(self.output_dir)

        self.source_single = os.path.join(
            self.source_dir, test_paths["source file"])
        self.target_single = os.path.join(
            self.target_dir,  test_paths["target file"])
        self.output_single = os.path.join(
            self.output_dir, test_paths["custom name"])

        self.http_source = test_paths["http source"]
        self.http_target = test_paths["http target"]

        self.source_file_http = os.path.join(
            self.source_dir, test_paths["source file http"])
        self.target_file_http = os.path.join(
            self.target_dir, test_paths["target file http"])

        self.save = ARGV["save"][0]
        self.show = ARGV["show"][0]

        self.width = "200"
        self.width_DEFAULT = IMAGES_SIZES["default width"]  # It's no arg
        self.width_too_low = str(
            IMAGES_SIZES["smallest dimension"] - 1)  # It's arg
        self.width_too_high = str(
            IMAGES_SIZES["biggest dimension"] + 1)  # It's arg

        self.by_ratio = test_paths["by ratio"]
        self.show_differences = ARGV['show differences'][0]

        self.refresh_folder = True

        self.target_fail = os.path.join(
            self.target_dir, test_paths["custom name"])

        self.source_dir_fail = self.source_dir + "Null"
        self.target_dir_fail = self.target_dir + "Nana"
        self.output_dir_fail = self.output_dir + "Zero"
        self.http_source_fail = self.http_source + "Void"

        self.random = test_paths["random"]

    def test_folder_by_folder_to_folder_save(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir]

        test_save_mode(self, _argv, 2)

    def test_folder_by_folder_to_single_save(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_single]

        test_save_mode(self, _argv, 2)

    def test_folder_by_folder_to_folder_save_width(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width]

        test_save_mode(self, _argv, 2)

    def test_http_by_folder_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.target_dir, self.save, self.output_dir]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_to_single_save(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_single]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_to_single_save_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_single, self.width]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_to_folder_save(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_dir]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_to_folder_save_show_differences(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_dir, self.show_differences]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_to_folder_save_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.save, self.output_dir, self.width]

        test_save_mode(self, _argv, 1)

    def test_http_by_single_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_dir]

        test_save_mode(self, _argv, 1)

    def test_http_by_single_to_folder_save_width(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_dir, self.width]

        test_save_mode(self, _argv, 1)

    def test_http_by_single_to_single_save(self):

        _argv = [program_name, self.http_source,
                 self.target_file_http, self.save, self.output_single]

        test_save_mode(self, _argv, 1)

    def test_http_by_http_to_folder_save(self):

        _argv = [program_name, self.http_source,
                 self.http_target, self.save, self.output_dir]

        test_save_mode(self, _argv, 1)

    def test_single_by_http_to_folder_save(self):

        _argv = [program_name, self.source_file_http,
                 self.http_target, self.save, self.output_dir]

        test_save_mode(self, _argv, 1)

    def test_http_by_http_to_single_save(self):

        _argv = [program_name, self.http_source,
                 self.http_target, self.save, self.output_single]

        test_save_mode(self, _argv, 1)

    def test_single_by_single_show(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.show]

        test_show_mode(self, _argv, 1)

    def test_single_by_single_show_width(self):

        _argv = [program_name, self.source_single,
                 self.target_single, self.show, self.width]

        test_show_mode(self, _argv, 1)

    def test_folder_by_folder_show(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show]

        test_show_mode(self, _argv, 2)

    def test_single_by_folder_show(self):

        _argv = [program_name, self.source_single,
                 self.target_dir, self.show]

        test_show_mode(self, _argv, 1)

    def test_http_by_folder_show(self):

        _argv = [program_name, self.http_source,
                 self.target_dir, self.show]

        test_show_mode(self, _argv, 1)

    def test_folder_by_folder_save_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.by_ratio]

        test_save_mode(self, _argv, 3)

    def test_folder_by_folder_save_width_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width, self.by_ratio]

        test_save_mode(self, _argv, 3)

    def test_folder_by_folder_show_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.by_ratio]

        test_show_mode(self, _argv, 3)

    def test_folder_by_folder_show_width_by_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width, self.by_ratio]

        test_show_mode(self, _argv, 3)

    def test_folder_by_folder_show_differences(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width, self.by_ratio, self.show_differences]

        test_show_mode(self, _argv, 3)

    def test_FAIL_file_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_fail, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['no file']}\n"
                         f" {self.target_fail}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_too_small_number_of_args(self):

        _argv = [program_name, self.source_dir, self.show]

        error_message = (f"{help_command_line()}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_no_output_file(self):

        _argv = [program_name, self.source_dir, self.target_dir, self.save]

        error_message = (f"{ERRORS_MESSAGES['no output']}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_4th_argument_random(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.random]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n" +
                         f"{self.random}\n" +
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_5th_argument_random(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.random]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n" +
                         f"{self.random}\n" +
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_6th_argument_random(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width, self.random]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n"
                         f"{self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_directory_with_target_references_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir_fail, self.show]

        error_message = (f"{get_error_directory_does_not_exists('target references')}\n"
                         f" {self.target_dir_fail}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_directory_with_source_references_does_not_exists(self):

        _argv = [program_name, self.source_dir_fail,
                 self.target_dir, self.show]

        error_message = (f"{get_error_directory_does_not_exists('source references')}\n"
                         f" {self.source_dir_fail}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_output_directory_does_not_exists(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir_fail]

        error_message = (f"{ERRORS_MESSAGES['output does not exists']}\n"
                         f" {self.output_dir_fail}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_output_directory_is_URL(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.http_target]

        error_message = (f"{ERRORS_MESSAGES['cant be url']}\n"
                         f" {self.http_target}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_Modified_same_dirs(self):

        _argv = [program_name, self.source_dir,
                 self.source_dir, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['Source Target same']}\n"
                         f" {self.source_dir}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_more_than_Modified(self):

        _argv = [program_name, self.target_dir,
                 self.source_dir, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['Source > Target']}\n"
                         f" {self.target_dir}\n"
                         f" {self.source_dir}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_Modified_same_files(self):

        _argv = [program_name, self.source_single,
                 self.source_single, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['Source Target same files']}\n"
                         f" {self.source_single}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_dir_Modified_file(self):

        _argv = [program_name, self.source_dir,
                 self.target_single, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['Source dir Target file']}\n"
                         f" {self.source_dir}\n"
                         f" {self.target_single}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_http_Error_404(self):

        _argv = [program_name, self.http_source_fail,
                 self.target_dir, self.save, self.output_dir]

        error_message = (f"{ERRORS_MESSAGES['404']}\n"
                         f" {self.http_source_fail}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_5th_random_6th_ratio(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.random, self.by_ratio]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n"
                         f"{self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_4th_random_5th_numeric(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.random, self.by_ratio]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n"
                         f"{self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_5th_width_6th_random(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width, self.random]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n"
                         f"{self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_one_too_much(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.show, self.width, self.by_ratio, self.random]

        error_message = (f"{ERRORS_MESSAGES['invalid arg']}\n"
                         f"{self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_not_mode(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.random]

        error_message = (f"{ERRORS_MESSAGES['not mode']}\n"
                         f" {self.random}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_width_too_low(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width_too_low]

        error_message = (get_error_width_too_low(self.width_too_low))

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_width_too_high(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.output_dir, self.width_too_high]

        error_message = (get_error_width_too_high(self.width_too_high))

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_no_images(self):

        _argv = [program_name, self.output_dir,
                 self.target_dir, self.show]

        error_message = (f"{get_error_no_images_in_dir('source references')}\n"
                         f" {self.output_dir}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_Source_same_as_output(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.source_dir]

        error_message = (f'{ERRORS_MESSAGES["output same as source"]}\n'
                         f" {self.source_dir}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)

    def test_FAIL_target_same_as_output(self):

        _argv = [program_name, self.source_dir,
                 self.target_dir, self.save, self.target_dir]

        error_message = (f'{ERRORS_MESSAGES["output same as target"]}\n'
                         f" {self.target_dir}\n"
                         f"{help_tip()}")

        test_FAIL_argv(self, _argv, error_message)


if __name__ == '__main__':
    unittest.main()
