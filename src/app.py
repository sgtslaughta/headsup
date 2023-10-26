import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("headsup")
        self.geometry("1000x600")
        self.resizable(False, False)