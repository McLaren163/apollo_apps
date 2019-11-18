import PySimpleGUI as sg
import tkinter as tk
import os
import subprocess
import sys
from pymitter import EventEmitter


class ShiftGateView(EventEmitter):
    def __init__(self, config):
        super().__init__()
        self.cfg = config
        pdf_creator = config.get('pdf_creator')
        if pdf_creator == 'fpdf':
            from src.fpdf_creator import PDFShiftgate 
            self._pdf_creator = PDFShiftgate
        if pdf_creator == 'xhtml2pdf':
            from src.html2pdf_creator import xhtml2pdf
            self._pdf_creator = xhtml2pdf

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

    def openResultFile(self, filename):
        """ open pdf file """
        if sys.platform == 'win32':
            os.startfile(filename)
        else:
            subprocess.call(['xdg-open', filename])

    def showResult(self, data):
        """
        create and open pdf file from data
        """
        # get name for pdf file
        pdf_name = self._choose_filename(self._getInitialFilename(data))
        print('View.showResult:', pdf_name)
        # create pdf file
        if pdf_name:
            self._createPdfFile(data, pdf_name)
            # show created file
            self.openResultFile(pdf_name)

    def showErrors(self, errors):
        print('Errors')

    def _createPdfFile(self, data, file_name):
        """
        create pdf object and save to file
        """
        self._pdf_creator(data).save(file_name)

    def _getInitialFilename(self, data):
        order = data.get('order', 'XXX')
        customer = data.get('customer', 'XXXXXXXX')
        initial_file = '{}-{}'.format(order,
                                      customer)
        return initial_file

    def _choose_filename(self, initialfile):
        """
        return file name
        """
        ftypes = [('Document PDF', '*.pdf'), ]
        file_name = tk.filedialog.asksaveasfilename(filetypes=ftypes,
                                                    initialfile=initialfile,
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
