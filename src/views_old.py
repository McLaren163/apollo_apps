import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from src.quitter import setAskOnCloseWin
from src.widgets import InputsBlockFrame, AboutLabel, Input
from pymitter import EventEmitter
from src.pdf_creator import PDFShiftgate


def getCallback(emitter, value_id, name_event='new value'):
    """вернет функцию, которая будет вызывать событие name_event
    у объекта emitter и передаст в него {value_id: new_value}"""
    def wrap_callback(new_value):
        """событие при установке нового значения"""
        if not new_value:
            return
        props = {value_id: new_value}
        print(props)
        emitter.emit(name_event, props)
    return wrap_callback


class View(EventEmitter, tk.Frame):
    inputs = {}

    def __init__(self, config):
        super().__init__()
        setAskOnCloseWin(self.master)
        self.master.title(config['title'])
        self.master.iconbitmap(config['files']['icon'])
        self.config = config
        self.createWidgets()
        self.pack(fill=tk.X)

    def createWidgets(self):
        pass

    def setState(self, props):
        """props = {id: value}"""
        for id, value in props.items():
            if id in self.inputs:
                self.inputs[id].setValue(value)

    def getState(self):
        """return {id: value}"""
        props = {}
        for id, var in self.inputs.items():
            props[id] = var.getValue()
        return props

    def start(self):
        self.mainloop()


class ShiftGateView(View):
    """
    docstring for ShiftGateView
    """

    def __init__(self, args):
        super().__init__(args)

    def createWidgets(self):
        config = self.config
        inputs = config['inputs']
        font = config['fonts']['gui']
        font_block = config['fonts']['gui-bold']
        label_w = config['label_width']

        ############ нижний бар с кнопкой submit ############

        buttons_frame = tk.Frame(self)
        AboutLabel(buttons_frame, font=font).pack(
            side=tk.LEFT)

        button = tk.Button(buttons_frame, text='Чертеж',
                           font=font)
        button.bind('<Button-1>', self.submit)
        button.pack(side=tk.RIGHT, padx=1, pady=2)

        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ############ блоки ввода значений ############

        block = InputsBlockFrame(self, 'Информация о заказе',
                                       2, label_w, font, font_block)
        insertInputsInBlock(block, 0, inputs, self.inputs, self,
                            ['order',
                             'customer'])
        insertInputsInBlock(block, 1, inputs, self.inputs, self,
                            ['engineer',
                             'date'])

        block = InputsBlockFrame(self, 'Параметры ворот',
                                       2, label_w, font, font_block)
        insertInputsInBlock(block, 0, inputs, self.inputs, self,
                            ['width',
                             'full_width',
                             'console',
                             'frame',
                             'filling',
                             'color_type'])
        insertInputsInBlock(block, 1, inputs, self.inputs, self,
                            ['height',
                             'cliarance',
                             'side',
                             'kit',
                             'frame_color',
                             'filling_color'])

        block = InputsBlockFrame(self, 'Комплектация',
                                       2, label_w, font, font_block)
        insertInputsInBlock(block, 0, inputs, self.inputs, self,
                            ['reception_column',
                             'reception_column_height',
                             'reception_column_num',
                             'beam',
                             'lock'])
        insertInputsInBlock(block, 1, inputs, self.inputs, self,
                            ['console_column',
                             'console_column_height',
                             'console_column_num',
                             'rack',
                             'door',
                             'decor'])

        block = InputsBlockFrame(self, 'Комментарий',
                                       1, label_w, font, font_block)
        insertInputsInBlock(block, 0, inputs, self.inputs, self,
                            ['comments', ])

    def submit(self, event):
        self.emit('submit')

    def showResult(self, data):
        initial_filename = '{} - {}'.format(data.get('order'),
                                            data.get('customer'))
        pdf_name = choose_pdf_name(initial_filename)
        if pdf_name:
            self.createPdfFile(data, pdf_name)
            self.update()  # обновить интерфейс
            os.startfile(pdf_name)

    def createPdfFile(self, data, file_name):
        font = self.config['fonts']['pdf']
        pdf = PDFShiftgate(data, font)
        pdf.save(file_name)


def choose_pdf_name(initial_name):
    ftype = [('Document PDF', '*.pdf'), ]
    file_name = asksaveasfilename(filetypes=ftype,
                                  initialfile=initial_name,
                                  defaultextension='.pdf')
    return file_name


def insertInputsInBlock(block, col, conf, datadict, emitter, ids):
    for id in ids:
        datadict[id] = block.insertInputWidget(col, conf[id],
                                               getCallback(emitter, id))
    block.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
