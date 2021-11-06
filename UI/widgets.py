# Python libs
try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk
import webbrowser
import sys
import tkinter.scrolledtext as tkSrcl

# Internal libs
from Show_Images_Differences.config.config import IMAGES_SIZES, set_app_path

# tk_ToolTip_class101.py
# gives a Tkinter widget a tooltip as the mouse is above the widget
# tested with Python27 and Python34  by  vegaseat  09sep2014
# www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

# Modified to include a delay time by Victor Zaccardo, 25mar16


class CreateToolTip():
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.top_window = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y = self.widget.bbox("insert")[:2]
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.top_window = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.top_window.wm_overrideredirect(True)
        self.top_window.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.top_window, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        top_window = self.top_window
        self.top_window = None
        if top_window:
            top_window.destroy()


class About():
    """Pop-up window displaying information about creator and project"""

    def __init__(self):
        about = tk.Toplevel()
        about.title("About")
        about.iconbitmap(
            f"{set_app_path()}UI/images/info.ico")

        # main window
        pad_value = 20
        padding = tk.Frame(about, padx=pad_value, pady=pad_value)
        padding.pack()

        # consts
        justify = "w"
        y_space = (15, 0)
        width = (0, 150)
        label_font = 'Helvetica 9 bold'

        # Version
        numb = "2.0.0"
        version_label = tk.Label(padding, text="Version:", font=label_font)
        version_label.pack(anchor=justify, padx=width)
        version_numb = tk.Label(padding, text=f"{numb}")
        version_numb.pack(anchor=justify)

        # Licence
        _type = "MIT"
        license_label = tk.Label(padding, text="License:", font=label_font)
        license_label.pack(pady=y_space, anchor=justify)
        license_type = tk.Label(padding, text=f"{_type}")
        license_type.pack(anchor=justify)
        license_link = tk.Label(padding, text="license link",
                                fg="blue", cursor="hand2")
        license_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences/blob/master/docs/LICENSE"))
        license_link.pack(anchor=justify)

        # Project type
        project_label = tk.Label(padding,
                                 text="Project site:", font=label_font)
        project_label.pack(pady=y_space, anchor=justify)
        project_link = tk.Label(padding, text="GitHub link",
                                fg="blue", cursor="hand2")
        project_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences"))
        project_link.pack(anchor=justify)

        # How to contribute
        contribute_label = tk.Label(padding, text="How to contribute:",
                                    font=label_font)
        contribute_label.pack(pady=y_space, anchor=justify)
        contribute_link = tk.Label(
            padding, text="Contribute link", fg="blue", cursor="hand2")
        contribute_link.bind("<Button-1>", lambda e: self.callback(
            "https://github.com/Luk-kar/Show_Images_Differences/blob/master/docs/CONTRIBUTING.md"))
        contribute_link.pack(anchor=justify)

        # Contact
        contact = "lukkarcontact@gmail.com"
        contact_label = tk.Label(padding, text="Contact:", font=label_font)
        contact_label.pack(pady=y_space, anchor=justify)
        contact_link = tk.Label(padding, text=contact,
                                fg="blue")
        contact_link.pack(anchor=justify)

    def callback(self, url):
        webbrowser.open_new(url)


class HowUse():
    """Pop-up window displaying information about usage"""

    def __init__(self):
        how_use = tk.Toplevel()
        how_use.title("How to use")
        how_use.iconbitmap(
            f"{set_app_path()}UI/images/info.ico")

        # main window
        pad_value = 20
        padding = tk.Frame(how_use, padx=pad_value, pady=pad_value)
        padding.pack()

        # consts
        justify = "w"
        y_space = (0, 5)
        width = (0, 150)
        label_font = 'Helvetica 9 bold'

        text = f"""
1. Choose source images and target images paths to compare.
2. In the best case, images have to be the same size.
3. If sizes are different, you can check "Search by the same ratio". But then you will get artifacts in renders.
To avoid too big distortions, accepted ratios between compared images are from {IMAGES_SIZES["lowest scale"]} to {IMAGES_SIZES["highest scale"]}.
4. Choose output methods ("Save" or "Show"), with the provided path or not.
5. Set any width's display images between 1 and {IMAGES_SIZES["biggest dimension"]} (px value).
6. If you want to see marked areas of differences on images you can check "Mark differences on images".
7. Finally, push the "Match images" button to render results.
        """
        how_to_use_label = tk.Label(
            padding, text="How to use:", font=label_font)
        how_to_use_label.pack(anchor=justify, padx=width)
        how_to_use_content = tk.Label(
            padding, text=f"{text}", justify="left")
        how_to_use_content.pack(pady=y_space)


class ScrolledTextBox():
    """This is box which show scrollable list of strings"""

    def __init__(self, title, _list):
        box = tk.Tk()

        box.wm_title(title)

        TextBox = tkSrcl.ScrolledText(
            box, height='10', width='100', wrap=tk.WORD)

        for count, item in enumerate(_list):

            TextBox.insert(tk.END, f"{str(count).zfill(5)} {item}\n")

            # Pushes the scrollbar and focus of text to the end of the text input.

        TextBox.pack()

        tk.mainloop()
