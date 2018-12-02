import tkinter as tk
from tkinter.filedialog import asksaveasfilename
# from tkinter.simpledialog import askinteger, askstring
from tkinter.ttk import Combobox
# from tkinter import Notebook
# from PIL.ImageTk import PhotoImage, Image
# from config import *


class InputMixin():
    def getVariable(self):
        return {self.id: {
                    'text': self.text,
                    'var': self.var
                }}


class Input(InputMixin, tk.Frame):
    """
    parent - родительский виджет
    name - текст метки
    values - тип ввода данных, значение None для Entry или 
             значение ('value1','value2','value3') для ComboBox
    width - ширина метки
    font - шрифт
    """

    def __init__(self, parent, id, text=None, rows=None, values=None, width=None, font=None):
        self.id = id
        self.var = tk.StringVar()

        tk.Frame.__init__(self, parent)

        if text:
            lbl = tk.Label(self, text=(text + ':'),
                           anchor=tk.W, width=width, font=font)
            lbl.pack(side=tk.LEFT, pady=1)

        if not values:
            ent = tk.Entry(self, textvariable=self.var,
                           justify=tk.CENTER, font=font)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        elif values == '>Date<':
            tk.Button(self, text='...', font=font).pack(
                      side=tk.RIGHT)  # TODO настройить комманду на колендарь
            ent = tk.Entry(self, textvariable=self.var,
                           justify=tk.CENTER, font=font)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        elif values == '>Boolean<':
            ent = tk.Checkbutton(self, variable=self.var, onvalue=1, offvalue=0)
            ent.pack(expand=tk.YES)
        elif values == '>Text<':
            ent = tk.Text(
                self, height=rows, font=font, wrap=tk.WORD)
            ent.pack(fill=tk.X)
        else:
            cmbbox = Combobox(self, textvariable=self.var, justify=tk.CENTER, 
                              font=font, values=values, state='readonly')
            # cmbbox.current(0)
            cmbbox.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)


class InputsBlock(tk.LabelFrame):
    """
    param (именованные аргументы):
        name - заголовок блока
        columns - число столбцов в блоке
        inputs - описание блока (('имя1', None),
                                 ('имя2', ('значение1',
                                          'значение2',
                                          'значение3'))),
    """
    def __init__(self, parent, columns, input_name_width, input_font, 
                 block_font, props):
        super().__init__(parent, text=props['text'], font=block_font)
        self._makeWidgets(columns, input_name_width, input_font, props)

    def _makeWidgets(self, columns, input_name_width, font, props):
        # block_frame = tk.Frame(self)
        columns = getFrameColumns(self, columns)
        col_index = 0

        for input_props in props['inputs']:
            block = Input(parent=columns[col_index],
                          width=input_name_width,
                          font=font,
                          **input_props)
            block.pack(side=tk.TOP, fill=tk.X, padx=1, pady=1)
            col_index += 1
            if col_index >= len(columns):
                col_index = 0

    def getDict(self):
        pass


class TextBlock(tk.LabelFrame):
    def __init__(self, parent, input_font,
                 block_font, props):
        super().__init__(parent, text=props['text'], font=block_font)
        self._makeWidgets(input_font, props)

    def _makeWidgets(self, input_font, props):
        self.text = tk.Text(self, height=props['rows'], font=input_font, wrap=tk.WORD)
        self.text.pack(fill=tk.X)

    def getDict(self):
        result = []
        text = self.text.get('1.0', 'end')
        text = text.strip()
        col = []
        for line in text.split('\n'):
            if line:
                col.append(line)
        result.append(col)
        return {self.name: result}


def getFrameColumns(parent, number):
    frames = []
    for n in range(int(number)):
        parent.columnconfigure(n, weight=1)
        fr = tk.Frame(parent)
        fr.grid(row=0, column=n, sticky='new', padx=3, pady=3)
        frames.append(fr)
    return frames


class PreviewWin(tk.Toplevel):
    def __init__(self, title, image, filename='New file', icon=None):
        super().__init__()
        if icon:
            self.iconbitmap(icon)
        self.filename = filename
        self.title(title)
        self.image = image
        preview = image.resize((600, 800), Image.ADAPTIVE)
        self.thumbs = PhotoImage(preview)
        self._makeWidgets()
        self.configure(width=600, height=600)  # TODO установить размер окна по дефолту
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def _makeWidgets(self):
        pass

    def handlerSave(self):
        ftype = [('Document PDF', '*.pdf'), ('Image PNG', '*.png')]
        file = asksaveasfilename(filetypes=ftype,
                                 initialfile=self.filename,
                                 defaultextension='.pdf')
        if file:
            if file.endswith('pdf'):
                out_image = self.image.resize((2000, 2829), Image.ADAPTIVE)
                im = out_image.convert('RGB')
                im.save(file, 'PDF')
            else:
                self.image.save(file, 'PNG')


class AboutLabel(tk.Label):
    def __init__(self, parent, **props):
        super().__init__(parent, **props)
        self.configure(text='Apollo | Makarov A.S.',
                       anchor=tk.W, fg='#555555', relief=tk.GROOVE)
