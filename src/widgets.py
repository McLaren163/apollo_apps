import tkinter as tk
from tkinter.filedialog import asksaveasfilename
# from tkinter.simpledialog import askinteger, askstring
from tkinter.ttk import Combobox
# from tkinter import Notebook
# from PIL.ImageTk import PhotoImage, Image
# from config import *

# под вопросом нужен ли?
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

    def __init__(self, parent, id, text=None, rows=None, values=None,
                 label_width=None, font=None):
        self.id = id
        self.var = None

        tk.Frame.__init__(self, parent)

        if text:
            lbl = tk.Label(self, text=(text + ':'),
                           anchor=tk.W, width=label_width, font=font)
            lbl.pack(side=tk.LEFT, pady=1)

        if not values:
            self.var = tk.StringVar()
            ent = tk.Entry(self, textvariable=self.var,
                           justify=tk.CENTER, font=font)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        # elif values == '>Date<':
        #     tk.Button(self, text='...', font=font).pack(
        #               side=tk.RIGHT)  # TODO настройить комманду на колендарь
        #     ent = tk.Entry(self, textvariable=self.var,
        #                    justify=tk.CENTER, font=font)
        #     ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        elif values == '>Boolean<':
            self.var = tk.BooleanVar()
            ent = tk.Checkbutton(self, variable=self.var, onvalue=1, offvalue=0)
            ent.pack(expand=tk.YES)
        elif values == '>Text<':
            ent = tk.Text(
                self, height=rows, font=font, wrap=tk.WORD)
            ent.pack(fill=tk.X)
            self.var = TextVar(ent)
        else:
            self.var = tk.StringVar()
            ent = Combobox(self, textvariable=self.var, justify=tk.CENTER,
                              font=font, values=values, state='readonly')
            # ent.current(0)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

    def getVar(self):
        return {self.id: self.var}


class TextVar():
    """Объект переменной значения для виджета Text"""
    def __init__(self, text_widget):
        self.text = text_widget

    def get(self):
        return self.text.get('1.0', 'end').strip()

    def set(self, value):
        self.text.delete(1.0, 'end')
        self.text.insert(1.0, value)


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
        self.vars = {}
        self._makeWidgets(columns, input_name_width, input_font, props)

    def _makeWidgets(self, columns, input_name_width, font, props):
        # block_frame = tk.Frame(self)
        columns = getFrameColumns(self, columns)
        col_index = 0

        for input_props in props['inputs']:
            block = Input(parent=columns[col_index],
                          label_width=input_name_width,
                          font=font,
                          **input_props)
            block.pack(side=tk.TOP, fill=tk.X, padx=1, pady=1)
            self.vars.update(block.getVar())
            col_index += 1
            if col_index >= len(columns):
                col_index = 0

    def getVars(self):
        return self.vars.copy()


def getFrameColumns(parent, number):
    frames = []
    for n in range(int(number)):
        parent.columnconfigure(n, weight=1)
        fr = tk.Frame(parent)
        fr.grid(row=0, column=n, sticky='new', padx=3, pady=3)
        frames.append(fr)
    return frames


class AboutLabel(tk.Label):
    def __init__(self, parent, **props):
        super().__init__(parent, **props)
        self.configure(text='Apollo | Makarov A.S.',
                       anchor=tk.W, fg='#555555', relief=tk.GROOVE)


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


