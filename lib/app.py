import tkinter as tk
from .utils import NetConns as Nc
from socket import gethostname


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"headsup - {gethostname()}")
        self.resizable(True, False)
        self.img = tk.PhotoImage(file="lib/img/vision.png")
        self.iconphoto(False, self.img)
        self.window = Window(self)
        self.menu = Menu(self)


class Window:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(self.app)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.net_win = Nc(self.frame)
        self.refresh_val = 1
        self.refresh_frame = tk.Frame(self.frame)
        self.refresh_frame.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.refresh_label = tk.Label(self.refresh_frame, text="Refresh Rate (s):")
        self.refresh_label.grid(row=0, column=0, sticky=tk.W)
        self.refresh_entry = tk.Entry(self.refresh_frame, width=5)
        self.refresh_entry.grid(row=0, column=1, sticky=tk.E)
        self.refresh_entry.insert(0, "1")
        self.refresh_button = tk.Button(self.refresh_frame, text="Refresh",
                                        command=self.refresh)
        self.refresh_button.grid(row=0, column=2, sticky=tk.E)
        self.info_label = tk.Label(self.frame)
        self.info_label.grid(row=3, column=0, sticky=tk.W)

        self.frame.after(1000, self.validate_refresh)
        self.frame.after(1000, self.refresh)

    def refresh(self):
        self.net_win.refresh_connections()
        self.frame.after(self.refresh_val * 1000, self.refresh)
        #self.info_label.config(text="Refreshed.", foreground="green")

    def validate_refresh(self):
        try:
            refresh = int(self.refresh_entry.get())
            if refresh < 1:
                raise ValueError
            self.refresh_val = refresh
            self.info_label.config(text="", foreground="black")
        except ValueError:
            self.refresh_entry.delete(0, tk.END)
            self.refresh_entry.insert(0, "1")
            self.info_label.config(text="Invalid refresh, defaulting to 1 "
                                        "second.", foreground="red")
        self.frame.after(1000, self.validate_refresh)


class Menu:
    def __init__(self, app):
        self.app = app
        self.menu = tk.Menu(self.app)
        self.app.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Quit", command=self.app.destroy)
        self.view_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.dark_mode_var = tk.BooleanVar()
        self.view_menu.add_checkbutton(label="Dark Mode",
                                   command=self.toggle_dark_mode,
                                       onvalue=True,
                                       offvalue=False,
                                       variable=self.dark_mode_var)

    def toggle_dark_mode(self):
        style = tk.ttk.Style(self.app)
        items = [self.menu, self.file_menu, self.view_menu,
                 self.app.window.net_win.label,
                 self.app.window.info_label, self.app.window.refresh_label,
                 self.app.window.refresh_entry,
]
        if self.dark_mode_var.get():
            style.theme_use("clam")
            style.configure("Treeview", background="gray15",
                            foreground="green2", fieldbackground="gray15",
                            )
            style.configure("Treeview.Heading", relief="flat", background="gray15",
                            foreground="green2", fieldbackground="gray15",)
            style.map("Treeview.Heading", background=[("pressed", "!focus",
                                               "gray26"),
                                              ("active", "gray26")])
            style.configure("Scrollbar", background="gray15",
                            foreground="green2", fieldbackground="gray15"
                            )
            for item in items:
                item.config(background="gray15", foreground="green2")

            self.app.window.net_win.win.config(background="gray15")
            self.app.window.refresh_frame.config(background="gray15")
            self.app.window.refresh_button.config(background="gray15",
                                                    foreground="green2",
                                                    activebackground="gray26",
                                                    activeforeground="yellow")
            self.menu.config(background="gray15", foreground="green2",
                                activebackground="gray26",
                                activeforeground="yellow")
            self.file_menu.config(background="gray15",
                                                foreground="green2",
                                                activebackground="gray26",
                                                activeforeground="yellow")
            self.view_menu.config(background="gray15",
                                                foreground="green2",
                                                activebackground="gray26",
                                                activeforeground="yellow")
            self.app.window.net_win.scrollbar.config(background="gray15",
                                                  troughcolor="gray15")


        else:
            style.theme_use("classic")
            for item in items:
                item.config(background="gray85", foreground="black")

            self.app.window.net_win.win.config(background="gray85")
            self.app.window.refresh_frame.config(background="gray85")
            self.app.window.refresh_button.config(background="gray85",
                                                    foreground="black",
                                                    activebackground="gray26",
                                                    activeforeground="yellow")
            self.menu.config(background="gray85", foreground="black",
                                activebackground="gray80",
                                activeforeground="black")
            self.file_menu.config(background="gray85",
                                                foreground="black",
                                                activebackground="gray80",
                                                activeforeground="black")
            self.view_menu.config(background="gray85",
                                                foreground="black",
                                                activebackground="gray80",
                                                activeforeground="black")
            self.app.window.net_win.scrollbar.config(background="gray85",
                                                    troughcolor="gray85")

