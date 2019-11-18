import os
from fpdf import FPDF
from src.cfg.graphics import GATE_IMAGES
from .config import IMAGE_FOLDER

FONT_NAME = "IBMPlexMono-Regular"
FONT_FILE = "./res/fonts/IBMPlexMono-Regular.ttf"
FONT_SIZE = 10.0


class PDFShiftgate(FPDF):
    """ """
    left_margin = 20
    textline_h = 5

    block_header_logo_w = 65

    block_draft_x = left_margin
    block_draft_y = 35
    block_draft_h = 90

    block_main_x = left_margin
    block_main_y = 80

    block_compl_x = left_margin
    block_compl_y = block_main_y + textline_h * 7  # 6+1 rows in main block

    block_attention_x = left_margin
    block_attention_y = block_compl_y + textline_h * 8  # 7+1 rows in compl blc

    block_beamname_x = left_margin
    block_beamname_y = block_attention_y + textline_h * 2

    block_beam_x = block_beamname_x
    block_beam_y = block_beamname_y + textline_h
    block_beam_h = 40

    block_comments_x = block_beam_x
    block_comments_y = block_beam_y + block_beam_h + textline_h

    def __init__(self, data):
        super().__init__()
        print('PDFShiftgate.__init__:', data)
        self.data = data
        self.f_size = FONT_SIZE
        try:
            self.add_font(FONT_NAME, '', FONT_FILE, uni=True)
            self.set_font(FONT_NAME)
        except:
            print('EXEPTION: PDFShiftgate - Not set new font!')

        self.l_margin = self.left_margin
        self.r_margin = 5.0
        self.t_margin = 7.0
        self.b_margin = 5.0

    def header(self):
        # Effective page width and height
        epw = self.w - self.l_margin - self.r_margin

        self.ln()
        # render logo
        self.renderImage('apollo_logo.png',
                         self.l_margin,
                         self.t_margin,
                         h=10)

        self.set_font_size(self.f_size + 2.0)

        self.set_x(self.block_header_logo_w)
        header_text = 'Откатные ворота {}'.format(self.data.get('model'))
        self.cell(0, 10,
                  header_text,
                  border=0, align='C')
        self.ln()

        self.set_font_size(self.f_size)

        self.cell(epw // 6 * 4, 7, 'Заказчик: ' +
                  self.data.get('customer'), border=1, align='L')
        self.cell(0, 7, 'Заказ: ' +
                  self.data.get('order'), border=1, align='L')
        self.ln()

        self.cell(epw // 6 * 4, 7, 'Инженер: ' +
                  self.data.get('engineer'), border=1, align='L')
        self.cell(0, 7, 'Монтаж: ' + self.data.get('date'),
                  border=1, align='L')

    def save(self, file):
        self.createOnePage()
        self.createTwoPage()
        self.output(file, 'F')

    def createOnePage(self):
        self.add_page('P')
        self.set_font_size(self.f_size - 2.0)

        # self.renderDraft(self.data.get('draft_type'))

        self._renderMainParameters(self.data)
        self._renderComplectation(self.data)
        # self._renderCut()
        attentions = self.data.get('attentions')
        if attentions:
            self._renderAttentions(attentions)
        # self._renderBeamName(self.data.get('beam'), self.data.get('beam_l'))
        # self._renderBeam(self.data.get('beam'))
        # self._renderComments(self.data.get('comments'))

    def createTwoPage(self):
        pass

    def renderImage(self, image_name, x, y, w=0, h=0):
        if image_name:
            image_file = os.path.join(IMAGE_FOLDER, image_name)
            if os.path.exists(image_file):
                self.image(image_file, x=x, y=y, h=h, w=w)
                return
        # FIXME add errors message
        print('PDFShiftgate.renderImage: image_name is None or image_file not exist')

    def _renderMainParameters(self, values):
        self.set_xy(self.block_main_x, self.block_main_y)
        txt = """Откат: {side} (вид со двора)
Ширина проема: {width} мм
Рабочая часть: {work_width} мм
Общая длина: {full_width} мм
Консоль: {console} {console_width} мм
Высота полотна: {height} мм """
        self.multi_cell(0, self.textline_h, txt.format(**values), align='L')

    def _renderCut(self):
        pass

    def _renderComments(self, text):
        self.set_x(self.block_text_x)
        # self.set_font('', 'B')
        self.cell(0, self.textline_h, 'ПРИМЕЧАНИЕ:', ln=2)
        self.multi_cell(0, self.textline_h, text, align='L')
        # self.set_font('', '')

    def _renderDraft(self, draft_type):
        image_name = GATE_IMAGES['draft_files'].get(draft_type)
        self.renderImage(image_name,
                         x=self.block_draft_x,
                         y=self.block_draft_y,
                         h=self.block_draft_h)

    def _renderBeamName(self, beam_type, beam_length):
        txt = str(beam_type)
        if beam_length:
            txt = txt + ': ' + str(beam_length) + ' мм'

        self.set_xy(self.block_beamname_x, self.block_beamname_y)
        self.cell(self.block_beamname_w, self.textline_h, txt)

    def _renderBeam(self, beam_type):
        image_name = GATE_IMAGES['beam_files'].get(beam_type)
        self.renderImage(image_name,
                         x=self.block_beam_x,
                         y=self.block_beam_y,
                         w=self.block_beam_w)

    def _renderComplectation(self, values):
        self.set_xy(self.block_compl_x, self.block_compl_y)
        txt = """Рама: {frame} Цвет {frame_color} {color_type}
Заполнение: {filling} Цвет {filling_color}
Комплектация: {kit}
Столб приемный: {reception_column} {reception_column_height} мм {reception_column_num} шт
Столб от бокового качения: {console_column} {console_column_height} мм {console_column_num} шт
Зубчатая рейка: {rack} шт
Задвижка DH: {lock}"""
        self.multi_cell(0, self.textline_h, txt.format(**values), align='L')

    def _renderAttentions(self, attentions):
        self.set_xy(self.block_attention_x, self.block_attention_y)
        self.set_text_color(210, 0, 0)  # red text color
        # FIXME only first value to print
        txt = 'ВНИМАНИЕ: ' + str(attentions[0])
        self.cell(0, self.textline_h, txt)
        self.set_text_color(0, 0, 0)  # black text color
