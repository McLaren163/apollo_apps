import tkinter as tk
from src.quitter import setAskOnCloseWin


class View(tk.Frame):

    def __init__(self, width, height):
        super().__init__()
        setAskOnCloseWin(self.master)
        self.master.width = width
        self.master.height = height
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        pass
