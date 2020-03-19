import PySimpleGUI as sg
import tkinter as tk
import os
import subprocess
import sys
from pymitter import EventEmitter
from src import config as CFG


class ShiftGateView(EventEmitter):
    def __init__(self):
        super().__init__()
        pdf_creator = CFG.PDF.get('creator')
        if pdf_creator == 'fpdf':
            from src.fpdf_creator import PDFShiftgate 
            self._pdf_creator = PDFShiftgate
        else:
            pass  # FIXME raise exeption

    def run(self, state=None):
        # create main window
        title = CFG.GUI.get('title')
        icon = CFG.FILES.get('icon')
        font = CFG.GUI.get('fonts').get('normal')
        sg.SetOptions(button_color=('black','lightgray'),
                      font=font,
                      margins=(2,1))
        layout = self._create_layout()
        self.window = sg.Window(title,
                                icon=icon,
                                element_padding=(0, 1)).Layout(layout)

        if state:
            self.set_state(state)

        # run main event loop
        while True:
            event, values = self.window.Read()
            if event is None:
                break   # exit
            elif event == 'submit_key':
                filename = self.get_filename(self._get_initial_filename(values))
                print(filename)
                if filename:
                    values['filepath'] = filename
                    self.emit('submit', values)

        self.window.Close()

    def _create_layout(self):
        order_c0 = [
            get_form('order'),
            get_form('customer')
        ]
        order_c1 = [
            get_form('date'),
            get_form('engineer')
        ]
        gate_c0 = [
            get_form('model'),
            get_form('width'),
            get_form('height'),
            get_form('cliarance'),
            get_form('full_width'),
            get_form('side'),
            get_form('console'),
        ]
        gate_c1 = [
            get_form('kit'),
            get_form('frame'),
            get_form('frame_color'),
            get_form('filling'),
            get_form('filling_color'),
            get_form('color_type'),
        ]
        complectation_c0 = [
            get_form('rack'),
            get_form('beam'),
            get_form('adjustments'),
        ]
        complectation_c1 = [
            get_form('lock'),
            get_form('door'),
            get_form('decor'),
        ]
        columns_c0 = [
            get_form('reception_column'),
            get_form('reception_column_height'),
            get_form('reception_column_num'),
        ]
        columns_c1 = [
            get_form('console_column'),
            get_form('console_column_height'),
            get_form('console_column_num'),
        ]
        order_layout = [
            [sg.Column(order_c0), sg.Column(order_c1)],
        ]
        gate_layout = [
            [sg.Column(gate_c0), sg.Column(gate_c1)],
        ]
        complectation_layout = [
            [sg.Column(complectation_c0), sg.Column(complectation_c1)]
        ]
        column_layout = [
            [sg.Column(columns_c0), sg.Column(columns_c1)],
        ]
        comment_layout = [
            get_form('comments'),
        ]

        # main layout
        layout = [
            [sg.Frame('Информация о заказе', order_layout, pad=(0,0))],
            [sg.Frame('Параметры ворот', gate_layout)],
            [sg.Frame('Комплектация', complectation_layout)],
            [sg.Frame('Столбы', column_layout)],
            [sg.Frame('Комментарий', comment_layout)],
            [sg.Button('Чертёж', key='submit_key')],
        ]

        return layout

    def set_state(self, values):
        """
        set all new values to view
        """
        self.window.Fill(values)

    def open_result_file(self, filename):
        """ open pdf file """
        if sys.platform == 'win32':
            os.startfile(filename)
        else:
            subprocess.call(['xdg-open', filename])

    def show_result(self, filename):
        """
        pdf file from data
        """
        if os.path.isfile(filename):
            self.open_result_file(filename)
        else:
            message = 'Файл {} не найден!'.format(filename)
            self.show_errors(message)

    def show_errors(self, *errors):
        print(errors)
        sg.PopupError(*errors, title='Ошибка')

    def _get_initial_filename(self, data):
        order = data.get('order', 'XXX')
        customer = data.get('customer', 'XXXXXXXX')
        initial_filename = '{}-{}.pdf'.format(order,
                                      customer)
        return initial_filename

    def get_filename(self, initial_name):
        """
        return file name
        """
        file_types = (('Document PDF', '*.pdf'), )

        file_name = tk.filedialog.asksaveasfilename(title='Select file to save',
                                                    filetypes=file_types,
                                                    initialdir=CFG.HOMEDIR,
                                                    initialfile=initial_name,
                                                    defaultextension='.pdf')

        return file_name


def get_form(_id, submit=False):
    gui = CFG.GUI
    widgets = CFG.WIDGETS
    s_txt = gui['size_text']
    s_inp = gui['size_input']
    s_cmb = gui['size_combo']
    s_mul = gui['size_multiline']
    element = widgets[_id]
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
