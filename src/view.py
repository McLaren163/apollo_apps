
import tkinter as tk
from src.quitter import setAskOnCloseWin
from src.widgets import InputsBlock, AboutLabel


class View(tk.Frame):
    vars = {}

    def __init__(self, config):
        super().__init__()
        setAskOnCloseWin(self.master)
        self.master.title('Откатные ворота "АПОЛЛО"')
        self.master.iconbitmap(config['files']['icon'])
        self.create_widgets(config)
        self.pack(fill=tk.X)

    def create_widgets(self, config):
        buttons_frame = tk.Frame(self)
        AboutLabel(buttons_frame, font=config['fonts']['gui']).pack(
            side=tk.LEFT)
        button = tk.Button(buttons_frame, text='Чертеж',
                  font=config['fonts']['gui'])
        button.bind('<Button-1>', self.onclick)
        button.pack(side=tk.RIGHT, padx=1, pady=2)
        
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        blocks = config['blocks']

        bl = InputsBlock(self, 2, config['label_width'], config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    blocks['order'])
        self.vars.update(bl.getVars())
        bl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)

        bl = InputsBlock(self, 2, config['label_width'], config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    blocks['product'])
        self.vars.update(bl.getVars())
        bl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        bl = InputsBlock(self, 2, config['label_width'], config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    blocks['options'])
        self.vars.update(bl.getVars())
        bl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        bl = InputsBlock(self, 1, None, config['fonts']['gui'],
                    config['fonts']['gui-bold'],
                    blocks['comments'])
        self.vars.update(bl.getVars())
        bl.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)

    def onclick(self, event):
        self.vars['order'].set('new order')
        self.vars['comments'].set('new value')
        self.vars['door'].set(False)
