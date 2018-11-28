
import tkinter as tk
from src.quitter import setAskOnCloseWin
from src.widgets import InputsBlock


class View(tk.Frame):

    def __init__(self, config):
        super().__init__()
        setAskOnCloseWin(self.master)
        self.master.title('Откатные ворота "АПОЛЛО"')
        self.master.iconbitmap(config['files']['icon'])
        self.create_widgets(config)
        self.pack()

    def create_widgets(self, config):
        InputsBlock(self,
                    config['label_width'],
                    config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    config['blocks']['order']).pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        InputsBlock(self,
                    config['label_width'],
                    config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    config['blocks']['product']).pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
