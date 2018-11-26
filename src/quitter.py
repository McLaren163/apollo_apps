import tkinter as tk
from tkinter.messagebox import askokcancel


class Quitter(tk.Frame):
    def __init__(self, parent=None, **option):
        tk.Frame.__init__(self, parent)
        self.pack()
        btn = tk.Button(self, text='Quit',
                        command=lambda: askQuit(self), **option)
        btn.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH)


class QuitButton(tk.Button):
    def __init__(self, parent=None, **option):
        super().__init__(parent)
        self.config(text='Quit', command=lambda: askQuit(parent), **option)


def setAskOnCloseWin(root):
    root.protocol('WM_DELETE_WINDOW', lambda: askQuit(root))


def askQuit(root):
    ans = askokcancel('Подтверждение выхода', 'Закрыть программу?')
    if ans:
        root.quit()
