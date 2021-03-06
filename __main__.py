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
import sys

# Internal libs
from manage import execute_from_command_line

if __name__ == "__main__":
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Program crashed; press Enter to exit")
