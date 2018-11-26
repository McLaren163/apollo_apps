import tkinter as tk
from tkinter.filedialog import asksaveasfilename
# from tkinter.simpledialog import askinteger, askstring
from tkinter.ttk import Combobox
# from tkinter import Notebook
from PIL.ImageTk import PhotoImage, Image
# from config import *


class LabelEntry(tk.Frame):
    """
    text - текст метки
    values - тип ввода данных, значение None для Entry или значение ('value1','value2','value3') для ComboBox
    """

    def __init__(self, parent, text, values=None, width=tk.LABEL_WIDTH):
        tk.Frame.__init__(self, parent)

        lbl = tk.Label(self, text=(text + ':'),
                       width=width, anchor=tk.W, font=FONT_DEF)
        lbl.pack(side=tk.LEFT)

        self.var = tk.StringVar()

        if not values:
            ent = tk.Entry(self, textvariable=self.var, justify=tk.CENTER, font=FONT_DEF)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        elif values == '>Date<':
            tk.Button(self, text='...', font=FONT_DEF).pack(
                side=tk.RIGHT)  # TODO настройить комманду на колендарь
            ent = tk.Entry(self, textvariable=self.var,
                           justify=tk.CENTER, font=FONT_DEF)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        else:
            cmbbox = Combobox(self, textvariable=self.var, justify=tk.CENTER, font=FONT_DEF,
                              values=values, state='readonly')
            #cmbbox.current(0)
            cmbbox.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)


class LabelEntryBlock(tk.Frame):
    """
    param (именованные аргументы):
        name - заголовок блока
        labels - описание блока ('имя1',
                                 'имя2',
                                ['имя3', ('значение1',
                                          'значение2',
                                          'значение3')],
    """
    def __init__(self, parent, **param):
        super().__init__(parent)
        self.name = param['name']
        tk.Label(self, text=self.name, font=FONT_BLOCK,
                 anchor=tk.W).pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        self._makeWidgets(param)

    def _makeWidgets(self, param):
        self.labels = {}
        self.vars = []
        for label in param['labels']:
            if type(label) is list:
                name = label[0]
                values = label[1]
            else:
                name = label
                values = None

            widget = LabelEntry(self, name, values)
            widget.pack(expand=tk.YES, fill=tk.X)
            self.labels[name] = widget.var

    def getDict(self):
        result = {}
        for key in self.labels:
            result[key] = self.labels[key].get()
        return result

    def setValues(self, values_dict):
        for key in values_dict:
            var = self.labels.get(key)
            if var:
                var.set(values_dict[key])


class ListBoxTable(tk.Frame):
    """
    column_names - имена столбцов таблицы
    """
    def __init__(self, parent, colunm_names):
        super().__init__(parent)

        frm_lbl = tk.Frame(self)
        frm_lbl.pack(expand=tk.YES, fill=tk.X)
        tk.Label(frm_lbl, text=colunm_names[0] + ':', anchor=tk.W,
                 font=FONT_DEF).pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

        frm_table = tk.Frame(self)
        frm_table.pack(expand=tk.YES, fill=tk.X)

        self.columns = []

        column_str = tk.Listbox(frm_table, selectmode=tk.SINGLE, font=FONT_DEF)
        column_str.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        column_str.bind('<Double-1>', self.handleColName)
        self.columns.append(column_str)

        for name_col in colunm_names[:0:-1]:
            tk.Label(frm_lbl, text=name_col + ':',
                     font=FONT_DEF).pack(side=tk.RIGHT)

            column_int = tk.Listbox(
                frm_table, selectmode=tk.SINGLE, 
                width=len(name_col), font=FONT_DEF)
            column_int.pack(side=tk.RIGHT)
            column_int.bind('<Double-1>', self.handleColNumber)
            self.columns.insert(1, column_int)

    def handleColName(self, event):
        self.askValue(event, askstring)

    def handleColNumber(self, event):
        self.askValue(event, askstring)  # askinteger

    def askValue(self, event, ask_func):
        widget = event.widget
        index = widget.curselection()
        if index:
            old_value = widget.get(index)
            value = ask_func('Ввод',
                             'Введите значение:',
                             initialvalue=old_value)
            if value:
                widget.delete(index)
                widget.insert(index, value)

    def addItem(self, item):
        if item:
            self.columns[0].insert('end', item)
            for col in self.columns[1:]:
                col.insert('end', '1')

    def removeItem(self):
        for col in self.columns:
            index = col.curselection()
            if index:
                for c in self.columns:
                    c.delete(index)
                break

    def get(self):
        return list(c.get(0, 'end') for c in self.columns)


class ListBoxTableBlock(tk.Frame):
    """
    param (именованные аргументы):
    name - заголовок блока
    column_names - имена колонок таблицы
    menu_items - список меню кнопки "+"
    """
    def __init__(self, parent, **param):
        super().__init__(parent)
        self.name = param['name']
        self.labels = param['column_names']
        tk.Label(self, text=self.name, font=FONT_BLOCK,
                 anchor=tk.W).pack(fill=tk.X)
        self._makeWidgets(param)

    def _makeWidgets(self, param):
        frm_button = tk.Frame(self)
        frm_button.pack(expand=tk.YES, fill=tk.X)

        self.table = ListBoxTable(self, self.labels)

        addButton = tk.Menubutton(frm_button, text=' + ',
                                  fg='green', font=FONT_BLOCK, relief=tk.FLAT)
        menu = tk.Menu(addButton, font=FONT_DEF, tearoff=False)
        self._createAddMenu(menu, param['menu_items'])
        addButton.configure(menu=menu)

        removeButton = tk.Button(frm_button, text='  -  ', fg='red', font=FONT_BLOCK, relief=tk.FLAT)
        removeButton.configure(command=lambda: self.table.removeItem())

        addButton.pack(side=tk.LEFT)
        removeButton.pack(side=tk.LEFT)
        self.table.pack(expand=tk.NO, fill=tk.X)

    def _createAddMenu(self, menu, items):
        for item in items:
            if type(item) == tuple:
                name, labels = item
                sub_menu = tk.Menu(menu, font=FONT_DEF, tearoff=False)
                self._createAddMenu(sub_menu, labels)
                menu.add_cascade(label=name, menu=sub_menu)
            elif item == '>Input<':
                menu.add_command(label='Другое...',
                                 command=lambda: self.table.addItem(
                                     askstring('Ввод', 'Наименование:')))
            else:
                menu.add_command(label=item,
                                 command=lambda it=item: self.table.addItem(it))

    def getDict(self):
        return {self.name: dict(zip(self.labels, self.table.get()))}


class TextBlock(tk.Frame):
    def __init__(self, parent, **param):
        super().__init__(parent)
        self.name = param['name']
        tk.Label(self, text=self.name, font=FONT_BLOCK, 
                 anchor=tk.W).pack(fill=tk.X)
        self._makeWidgets(param)

    def _makeWidgets(self, param):
        self.text = tk.Text(self, height=5, font=FONT_DEF, wrap=tk.WORD)
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
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(text='Powered by Makarov A.C.',
                       anchor=tk.W, fg='#555555', relief=tk.GROOVE)
