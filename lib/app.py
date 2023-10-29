import tkinter as tk
from .utils import NetConns as Nc


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("headsup")
        self.resizable(True, False)
        self.window = Window(self)
        self.menu = Menu(self)


class Window:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(self.app)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.net_win = Nc(self.frame)


class Menu:
    def __init__(self, app):
        self.app = app
        self.menu = tk.Menu(self.app)
        self.app.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Quit", command=self.app.destroy)
