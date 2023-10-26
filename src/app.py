import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("headsup")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.window = Window(self)


class Window:
    def __init__(self, app):
        self.app = app
        self.frame = tk.Frame(self.app)
        self.frame.pack()
        self.label = tk.Label(self.frame, text="Hello, World!")
        self.label.pack()
        self.button = tk.Button(self.frame, text="Quit", command=self.app.destroy)
        self.button.pack()
