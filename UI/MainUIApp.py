"""GUI to comunicate with Reference_Judge module"""

# Python libs
from configparser import ConfigParser
import os
from tkinter import filedialog  # for Python 3
from tkinter import messagebox
import tkinter as tk
import sys

# external libs
from cv2 import destroyAllWindows

# internal libs
from UI.widgets import CreateToolTip, About, HowUse
from Reference_Judge.config import IMAGES_SIZES, ARGV
from Reference_Judge.help import help_tip
from Reference_Judge.Reference_Judge import Reference_Judge


# https://stackoverflow.com/a/17466924/12490791
class MainGUIApp():
    def __init__(self):

        master = tk.Tk()

        master.title(sys.argv[0])
        window_width = 618
        window_height = 555
        master.geometry(f"{window_width}x{window_height}")

        # Create frames
        frame_matching = tk.LabelFrame(master, padx=10, pady=15)
        frame_matching.grid(row=0, column=0, padx=10, pady=(25, 15))

        frame_output = tk.LabelFrame(master, padx=10, pady=15)
        frame_output.grid(row=1, column=0, padx=10, pady=(15, 0))

        frame_optional = tk.LabelFrame(master, padx=10, pady=15)
        frame_optional.grid(row=2, column=0, padx=10, pady=(15, 0), stick="we")

        # Default path text field placeholder
        self.entry_text_placeholder = "Enter your path..."

        # Source
        self.source_label = tk.Label(frame_matching, text="Original refs:")
        self.source_label.grid(row=0, column=0, pady=(0, 5), stick="w")

        self.source_entry = self.create_path_entry(
            frame_matching,
            self.on_entry_click_source,
            self.on_focusout_source
        )
        self.source_entry.grid(row=1, column=0, ipadx=200,
                               pady=(0, 5), stick="we")

        # Images to buttons
        self.img_open_folder = tk.PhotoImage(
            file=f"{sys.argv[0]}/UI/images/open_folder.gif")
        self.img_open_file = tk.PhotoImage(
            file=f"{sys.argv[0]}/UI/images/open_file.gif")

        # Source buttons for path
        self.source_btn_folder = self.create_path_btn(
            frame_matching,
            self.source_btn_folder_open,
            self.img_open_folder
        )
        self.source_btn_folder.grid(row=1, column=2, padx=5)

        self.source_btn_file = self.create_path_btn(
            frame_matching,
            self.source_btn_file_open,
            self.img_open_file
        )
        self.source_btn_file.grid(row=1, column=3)

        # Target
        self.target_label = tk.Label(frame_matching, text="App refs:")
        self.target_label.grid(row=2, column=0, pady=(0, 5), stick="w")

        self.target_entry = self.create_path_entry(
            frame_matching,
            self.on_entry_click_target,
            self.on_focusout_target
        )
        self.target_entry.grid(row=3, column=0, ipadx=200,
                               pady=(0, 5), stick="we")

        # Target buttons for path
        self.target_btn_folder = self.create_path_btn(
            frame_matching,
            self.target_btn_folder_open,
            self.img_open_folder
        )
        self.target_btn_folder.grid(row=3, column=2)

        self.target_btn_file = self.create_path_btn(
            frame_matching,
            self.target_btn_file_open,
            self.img_open_file
        )
        self.target_btn_file.grid(row=3, column=3)

        # Save
        self.mode = tk.StringVar()
        self.mode.set(ARGV["save"][0])

        self.save_radio = tk.Radiobutton(frame_output,
                                         text="Save",
                                         variable=self.mode,
                                         value=ARGV["save"][0],
                                         command=self.set_state_output_entry
                                         )
        self.save_radio.grid(row=0, column=0, stick="w")

        # Output
        self.output_label = tk.Label(frame_output, text="Output files:")
        self.output_label.grid(row=1, column=0, pady=(0, 5), stick="w")

        self.output_entry = self.create_path_entry(
            frame_output,
            self.on_entry_click_output,
            self.on_focusout_output
        )
        self.output_entry.grid(row=2, ipadx=200, stick="we")

        # Output buttons for path
        self.output_btn_folder = self.create_path_btn(
            frame_output,
            self.output_btn_folder_open,
            self.img_open_folder
        )
        self.output_btn_folder.grid(row=2, padx=5, column=2)

        self.output_btn_file = self.create_path_btn(
            frame_output,
            self.output_btn_file_open,
            self.img_open_file
        )
        self.output_btn_file.grid(row=2, column=3)

        # Show
        self.show_radio = tk.Radiobutton(frame_output,
                                         text="Show",
                                         variable=self.mode,
                                         value=ARGV["show"][0],
                                         command=self.set_state_output_entry
                                         )
        self.show_radio.grid(row=3, column=0, pady=(13, 0), stick="w")

        # Width
        self.width_label = tk.Label(frame_optional, text="Width:")
        self.width_label.grid(row=0, column=0, pady=(0, 5), stick="w")

        self.width_text = tk.StringVar()  # the text in  your entry
        self.width_entry = tk.Entry(
            frame_optional, borderwidth=1, textvariable=self.width_text)
        self.width_entry.grid(row=1, column=0, pady=(0, 20), stick="w")

        # By ratio
        self.by_ratio = tk.StringVar()

        self.by_ratio_checkbox = tk.Checkbutton(
            frame_optional,
            text="Search by the same ratio",
            variable=self.by_ratio,
            onvalue=ARGV["search by ratio"][0],
            offvalue="default"
        )
        self.by_ratio_checkbox.deselect()
        self.by_ratio_checkbox.grid(row=2, column=0, stick="w")

        # Match images
        self.match_btn = tk.Button(
            master, text="Match images", bg="#f5f5f5", command=self.match_images_btn)
        self.match_btn.config(height=3)
        self.match_btn.grid(row=3, column=0, pady=(20, 0),
                            stick="we", padx=(10, 10))

        # populate dialogs with default values
        self.defaults_path = f"{sys.argv[0]}\\data\\appData\\_DEFAULT.ini"

        try:
            self.setup_reset_to_defaults(show_message=False)
        except IOError:
            # create new file if default does not exists
            self.setup_default_reset(show_message=False)

        self.create_menu(master)

        # run UI
        master.mainloop()

    # Menu Code

    def create_menu(self, master):

        self.add_tooltips_to_widgets()

        my_menu = tk.Menu(master)
        master.config(menu=my_menu)

        menu_setup = tk.Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Setup", menu=menu_setup)
        menu_setup.add_command(label="Save as", command=self.setup_save_as)
        menu_setup.add_command(label="Open", command=self.setup_open)
        menu_setup.add_command(label="Save to defaults",
                               command=self.setup_save)
        menu_setup.add_command(label="Reset to defaults",
                               command=self.setup_reset_to_defaults)
        menu_setup.add_command(label="Defaults reset",
                               command=self.setup_default_reset)
        menu_setup.add_separator()
        menu_setup.add_command(label="Exit", command=master.quit)

        menu_help = tk.Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="Help", menu=menu_help)
        menu_help.add_command(label="How to use", command=HowUse)
        menu_help.add_separator()
        menu_help.add_command(label="About", command=About)

    def setup_open(self):

        setup_file = filedialog.askopenfilename(
            initialdir=self.defaults_path,
            title="Save setup file",
            filetypes=[("Setup files", "*.ini")]
        )

        if not setup_file:
            return

        config = read_config_file(setup_file)

        self.dialogs_set_setup(config)

        # refocus from any other entry to no get editing placeholder text bug
        self.width_entry.focus()

    def dialogs_set_setup(self, config):

        self.source_entry = self.entry_set(
            self.source_entry, config.get("MATCHING", "source entry")
        )

        self.target_entry = self.entry_set(
            self.target_entry, config.get("MATCHING", "target entry")
        )

        mode_content = config.get("OUTPUT", "mode")
        self.mode.set(mode_content)
        self.set_state_output_entry()

        self.output_entry = self.entry_set(
            self.output_entry, config.get("OUTPUT", "output entry")
        )

        self.width_entry = self.entry_set_text(
            self.width_entry, config.get("OPTIONAL", "width entry"))

        by_ratio_state = config.get("OPTIONAL", "by the same ratio")
        self.by_ratio.set(by_ratio_state)

    def entry_set(self, entry, entry_content):

        entry = self.entry_set_text(entry, entry_content)

        if entry_content != self.entry_text_placeholder:
            entry.config(fg='black')
        else:
            entry.config(fg='grey')

        return entry

    def entry_set_text(self, entry, text):

        entry.delete(0, "end")
        entry.insert(
            0,
            text
        )

        return entry

    def setup_reset_to_defaults(self, show_message=True):

        defaults_file = self.defaults_path

        config = read_config_file(defaults_file)

        self.dialogs_set_setup(config)

        if show_message:
            messagebox.showinfo(
                "Done!",
                "You reset your setup to defaults"
            )

    def setup_default_reset(self, show_message=True):

        defaults_file = self.defaults_path

        setup_saving(
            defaults_file,
            "Enter your path...",
            "Enter your path...",
            ARGV["save"][0],
            "Enter your path...",
            IMAGES_SIZES["default width"],
            "default",
        )

        config = read_config_file(defaults_file)

        self.dialogs_set_setup(config)

        if show_message:
            messagebox.showinfo(
                "Done!",
                "You reset setup configuration to factory settings"
            )

    def setup_save(self):

        # to give user full path info
        output_path = os.path.join(
            os.getcwd(), self.defaults_path)

        setup_saving(
            output_path,
            self.source_entry.get(),
            self.target_entry.get(),
            self.mode.get(),
            self.output_entry.get(),
            self.width_entry.get(),
            self.by_ratio.get(),
        )

        messagebox.showinfo(
            "Done!",
            "You saved setup configuration to defaults"
        )

    def setup_save_as(self):

        ini_default_location = os.path.join(os.getcwd(), "data/appData")
        output_path = filedialog.asksaveasfilename(
            initialdir=ini_default_location,
            title="Save setup file",
            filetypes=[("Setup files", "*.ini")]
        )

        if output_path:
            setup_saving(
                output_path,
                self.source_entry.get(),
                self.target_entry.get(),
                self.mode.get(),
                self.output_entry.get(),
                self.width_entry.get(),
                self.by_ratio.get(),
            )

            messagebox.showinfo(
                "Done!",
                "You saved setup file in:"f"\n{output_path}"
            )

    # End Menu Code

    def add_tooltips_to_widgets(self):

        tooltips = {
            "entry_match": "Path of single file, dir or URL...",
            "entry_output": "Path of single file or dir...",
            "save": "Save matched images in chosen directory",
            "show": "Show matched images",
            "width": "Width of each separate image",
            "by_ratio": 'Match images refs: "Original -> App", ' +
            "with diffrent sizes but the same ratio.\n" +
            "Not recommended due to distortions.",
            "btn_folder": "Choose folder...",
            "btn_file": "Choose file...",
            "match_btn": "Run the script!"
        }

        CreateToolTip(self.source_entry, tooltips["entry_match"])
        CreateToolTip(self.target_entry, tooltips["entry_match"])
        CreateToolTip(self.output_entry, tooltips["entry_output"])
        CreateToolTip(self.width_entry, tooltips["width"])

        CreateToolTip(self.source_label, tooltips["entry_match"])
        CreateToolTip(self.target_label, tooltips["entry_match"])
        CreateToolTip(self.output_label, tooltips["entry_output"])
        CreateToolTip(self.width_label, tooltips["width"])

        CreateToolTip(self.save_radio, tooltips["save"])
        CreateToolTip(self.show_radio, tooltips["show"])

        CreateToolTip(self.by_ratio_checkbox, tooltips["by_ratio"])

        CreateToolTip(self.source_btn_file, tooltips["btn_file"])
        CreateToolTip(self.source_btn_folder, tooltips["btn_folder"])

        CreateToolTip(self.target_btn_file, tooltips["btn_file"])
        CreateToolTip(self.target_btn_folder, tooltips["btn_folder"])

        CreateToolTip(self.output_btn_file, tooltips["btn_file"])
        CreateToolTip(self.output_btn_folder, tooltips["btn_folder"])

        CreateToolTip(self.match_btn, tooltips["match_btn"])

    def create_path_entry(self, frame, FocusIn, FocusOut):

        entry = tk.Entry(frame, borderwidth=1)
        entry.bind('<FocusIn>', FocusIn)
        entry.bind('<FocusOut>', FocusOut)
        entry.config(fg='grey')

        return entry

    def create_path_btn(self, frame, command, image):

        button = tk.Button(frame, command=command)
        button.config(image=image)

        return button

    # Events functions   =============================================

    def on_entry_click_source(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.source_entry, self.entry_text_placeholder)

    def on_focusout_source(self, event):
        on_focusout(self.source_entry, self.entry_text_placeholder)

    def on_entry_click_target(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.target_entry, self.entry_text_placeholder)

    def on_focusout_target(self, event):
        on_focusout(self.target_entry, self.entry_text_placeholder)

    def on_entry_click_output(self, event):
        """function that gets called whenever entry is clicked"""
        on_entry_click(self.output_entry, self.entry_text_placeholder)

    def on_focusout_output(self, event):
        on_focusout(self.output_entry, self.entry_text_placeholder)

    # End: events functions   ========================================

    def source_btn_folder_open(self):

        btn_find_path(self.source_entry, filedialog.askdirectory)

    def source_btn_file_open(self):

        btn_find_path(self.source_entry, filedialog.askopenfilename)

    def target_btn_folder_open(self):

        btn_find_path(self.target_entry, filedialog.askdirectory)

    def target_btn_file_open(self):

        btn_find_path(self.target_entry, filedialog.askopenfilename)

    def output_btn_folder_open(self):

        btn_find_path(self.output_entry, filedialog.askdirectory)

    def output_btn_file_open(self):

        btn_find_path(self.output_entry, filedialog.askopenfilename)

    def set_state_output_entry(self):

        if self.mode.get() == ARGV["save"][0]:

            self.output_label.configure(state="normal")
            self.output_entry.configure(state="normal")
            self.output_btn_folder.configure(state="normal")
            self.output_btn_file.configure(state="normal")

        elif self.mode.get() == ARGV["show"][0]:

            self.output_label.configure(state="disabled")
            self.output_entry.configure(state="disabled")
            self.output_btn_folder.configure(state="disabled")
            self.output_btn_file.configure(state="disabled")
        else:
            raise ValueError(f"Not existing ARG:\n{self.mode.get()}")

    def match_images_btn(self):

        _argv = list()

        program_name = sys.argv[0]
        _argv.append(program_name)

        source = self.source_entry.get()
        if self.path_exists(source):
            _argv.append(source)

        target = self.target_entry.get()
        if self.path_exists(target):
            _argv.append(target)

        mode = self.mode.get()
        if self.mode_exists(mode):
            _argv.append(mode)

        output = self.output_entry.get()
        if self.path_exists(output) and mode == ARGV["save"][0]:
            _argv.append(output)

        width = self.width_entry.get()
        if self.width_exists(width):
            _argv.append(width)

        by_ratio = self.by_ratio.get()
        if by_ratio != "default":
            _argv.append(by_ratio)

        window_name = "Wrong input"
        if self.pop_up_invalid_entry_path(window_name, source, target, output, mode, width):
            return

        try:
            summary = Reference_Judge(_argv)
        except SystemExit as error:
            error_cleaned = str(error).replace(help_tip(), '')
            messagebox.showwarning(window_name, error_cleaned)
            return

        if mode == ARGV["show"][0]:
            destroyAllWindows()  # to avoid bug with not closing last window

        if mode == ARGV["save"][0]:
            messagebox.showinfo(
                "Done!", f"You saved images in:\n{output}\n\n{summary}")

    def path_exists(self, path):
        return path != self.entry_text_placeholder and isinstance(path, str)

    def mode_exists(self, mode):

        modes = [
            ARGV["save"][0],
            ARGV["show"][0]
        ]

        return mode in modes

    def width_exists(self, width):
        return width != str(IMAGES_SIZES["default width"])

    def pop_up_invalid_entry_path(self, window_name, source, target, output, mode, width):

        if not source or source == self.entry_text_placeholder:
            return messagebox.showwarning(window_name, "No original references")

        if not target or target == self.entry_text_placeholder:
            return messagebox.showwarning(window_name, "No app references")

        if mode == ARGV["save"][0] and (not output or output == self.entry_text_placeholder):
            return messagebox.showwarning(window_name, "No output path")

        if width == IMAGES_SIZES["default width"]:
            return messagebox.showwarning(window_name, "No width")

        if not width.isnumeric():
            return messagebox.showwarning(window_name, "Width should be positive integer")

        return None


def read_config_file(file):

    config = ConfigParser()

    try:
        with open(file) as f:
            config.read_file(f)
    except IOError as error:
        raise IOError(error)

    return config


def on_entry_click(entry, placeholder):
    """function that gets called whenever entry is clicked"""

    if entry.get() == placeholder:
        entry.delete(0, "end")  # delete all the text in the source_entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')


def on_focusout(entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')


def btn_find_path(entry, askpath):

    path = askpath()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)
        entry.config(fg='black')


def setup_saving(
    output_path,
    source_entry,
    target_entry,
    mode,
    output_entry,
    width_entry,
    by_ratio,
):

    config = ConfigParser()

    config["MATCHING"] = {
        "source entry": source_entry,
        "target entry": target_entry
    }

    config["OUTPUT"] = {
        "mode": mode,
        "output entry": output_entry
    }

    config["OPTIONAL"] = {
        "width entry": width_entry,
        "by the same ratio": by_ratio
    }

    if output_path:
        with open(output_path, "w") as configfile:
            config.write(configfile)
    else:
        raise OSError("There is no save path")
