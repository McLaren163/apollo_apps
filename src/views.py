import PySimpleGUI as sg
import tkinter as tk
import os
import subprocess
import sys
from pymitter import EventEmitter
from src.pdf_creator import PDFShiftgate


class ShiftGateView(EventEmitter):
    def __init__(self, config):
        super().__init__()
        self.cfg = config

    def run(self, state=None):
        # create main window
        title = self.cfg['title']
        icon = self.cfg['files']['icon']
        font = self.cfg['fonts']['gui']
        button_color = ('black', 'darkgrey')
        layout = self._createLayout(self.cfg)
        self.window = sg.Window(title, icon=icon, font=font,
                                element_padding=(0, 1),
                                button_color=button_color).Layout(layout)

        if state:
            self.setState(state)

        # run main event loop
        while True:
            event, values = self.window.Read()
            if event is None:
                break   # exit
            elif event == 'submit_key':
                self.emit('submit', values)

        self.window.Close()

    def _createLayout(self, layout_config):
        insert = insertInputFabric(layout_config)

        order_c0 = [
            insert('order'),
            insert('customer')
        ]
        order_c1 = [
            insert('engineer'),
            insert('date')
        ]
        gate_c0 = [
            insert('width'),
            insert('full_width'),
            insert('console', True),
            insert('frame'),
            insert('filling'),
            insert('filling_weight'),
        ]
        gate_c1 = [
            insert('height'),
            insert('cliarance'),
            insert('side'),
            insert('kit'),
            insert('frame_color'),
            insert('filling_color'),
            insert('color_type'),
        ]
        extra_c0 = [
            insert('reception_column'),
            insert('reception_column_height'),
            insert('reception_column_num'),
            insert('beam'),
            insert('rack'),
        ]
        extra_c1 = [
            insert('console_column'),
            insert('console_column_height'),
            insert('console_column_num'),
            insert('lock'),
            insert('door'),
            insert('decor'),
        ]
        order_layout = [
            [sg.Column(order_c0), sg.Column(order_c1)],
        ]
        gate_layout = [
            [sg.Column(gate_c0), sg.Column(gate_c1)],
        ]
        extra_layout = [
            [sg.Column(extra_c0), sg.Column(extra_c1)],
        ]
        comment_layout = [
            insert('comments'),
            # [sg.Multiline(size=self.cfg.get('size_multiline'))],
        ]

        # main layout
        layout = [
            [sg.Frame('Информация о заказе', order_layout)],
            [sg.Frame('Параметры ворот', gate_layout)],
            [sg.Frame('Комплектация', extra_layout)],
            [sg.Frame('Комментарий', comment_layout)],
            [sg.Button('Чертёж', key='submit_key')],
        ]
        return layout

    def setState(self, values):
        """
        set all new values to view
        """
        self.window.Fill(values)

    def showResult(self, data):
        """
        create and open pdf file from data
        """
        # get name for pdf file
        pdf_name = self._choose_filename(data)
        print('View.showResult:', pdf_name)
        # create pdf file
        if pdf_name:
            self._createPdfFile(data, pdf_name)
            # open pdf file
            if sys.platform == 'win32':
                os.startfile(pdf_name)
            else:
                subprocess.call(['xdg-open', pdf_name])

    def showErrors(self, errors):
        print('Errors')

    def _createPdfFile(self, data, file_name):
        """
        create pdf object and save to file
        """
        font = self.cfg['fonts']['pdf']
        pdf = PDFShiftgate(data, font=font)
        pdf.save(file_name)

    def _choose_filename(self, data):
        """
        return file name
        """
        order = data.get('order', 'XXX')
        customer = data.get('customer', 'XXXXXXXX')
        initial_file = '{}-{}'.format(order,
                                      customer)
        ftypes = [('Document PDF', '*.pdf'), ]
        file_name = tk.filedialog.asksaveasfilename(filetypes=ftypes,
                                                    initialfile=initial_file,
                                                    defaultextension='.pdf')
        return file_name


def insertInputFabric(config):
    def wrap(_id, submit=False):
        return insertInput(_id, submit, config)
    return wrap


def insertInput(_id, submit, config):
    s_txt = config['size_text']
    s_inp = config['size_input']
    s_cmb = config['size_combo']
    s_mul = config['size_multiline']
    element = config['inputs'][_id]
    res = []

    text = element.get('text')
    if text:
        res.append(sg.Text(text, size=s_txt, pad=(0, 4)))
    values = element.get('values')
    if not values:
        res.append(sg.Input(size=s_inp, key=_id, change_submits=submit))
    elif values == '>Text<':
        res.append(sg.Multiline(size=s_mul, key=_id, change_submits=False))
    elif values == '>Boolean<':
        res.append(sg.Checkbox('', key=_id, change_submits=submit))
    elif isinstance(values, (list, tuple)):
        res.append(sg.Combo(values, size=s_cmb, default_value=' ', key=_id,
                            change_submits=submit))
    return res
