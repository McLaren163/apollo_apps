import os
from fpdf import FPDF
from src import config as CFG
from src.exeptions import FileNotExistError

FONT_NAME = "STSEV"
FONT_FILE = CFG.FILES.get('font-stsev')
FONT_SIZE = 14.0

LOGO_FILE = CFG.FILES.get('logo')

TMPL_GATE = """Параметры проема:
  Ширина проема: {width} мм
  Высота проема: {height} мм
  Просвет: {cliarance} мм

Параметры полотна:
  Ширина полотна: {full_width} мм
  Высота полотна:  мм
  Рабочая часть: {work_width} мм
  Консольная часть: {console_width} мм
  Откат (вид содвора): {side}
  Система: {kit}
  Рама: {frame}
  Цвет рамы: {frame_color}"""

TMPL_FILL = """Заполнение:
  Вид заполнения: {filling}
  Размер заполнения: мм
  Цвет заполнения: {filling_color}
  Структура краски: {color_type}

Комплектация:
  Столб приемный: {reception_column} {reception_column_height}мм {reception_column_num}шт
  Столб от бокового качения: {console_column} {console_column_height}мм {console_column_num}шт
  Зубчатая рейка: {rack}шт
  Опорная балка: {beam}
  Подставки регулировочные: {adjustments}
  Ручка:
  Задвижка: {lock}"""

TMPL_COMMENT = """Примечание:
  {comments}"""


class PDFShiftgate(FPDF):
    """ """
    left_margin = 20
    textline_h = 5

    block_logo_x = 150
    block_logo_y = 7
    block_logo_h = 10

    block_sketch_a_x = left_margin
    block_sketch_a_y = 32
    block_sketch_a_h = 86

    block_txt1_x = left_margin + 5
    block_txt1_y = block_sketch_a_y + block_sketch_a_h  # + textline_h

    block_txt2_x = block_txt1_x + 60
    block_txt2_y = block_txt1_y

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
        eph = self.h - self.t_margin - self.b_margin

        self.ln()
        # render logo
        self.renderImage(LOGO_FILE, self.block_logo_x, self.block_logo_y, h=10)

        self.set_font_size(self.f_size + 2.0)
        model = self.data.get('model').upper()
        header_text = 'ОТКАТНЫЕ ВОРОТА серии {}'.format(model)
        self.cell(0, 10,
                  header_text,
                  border=0, align='L')
        self.ln()

        self.set_font_size(self.f_size)

        self.cell(epw // 4, 7, 'Заказ: ' +
                  self.data.get('order'), border=1, align='L')
        self.cell(0 , 7, 'Заказчик: ' +
                  self.data.get('customer'), border=1, align='L')
        self.ln()

        self.cell(epw // 4, 7, 'Монтаж: ' + self.data.get('date'),
                  border=1, align='L')
        self.cell(0, 7, 'Инженер: ' +
                  self.data.get('engineer'), border=1, align='L')

        # render main rectangle
        self.rect(self.l_margin, self.t_margin, epw, eph)

    def save(self, file):
        self.create_page_one()
        self.create_page_two()
        self.output(file, 'F')

    def create_page_one(self):
        self.add_page('P')
        self.set_font_size(self.f_size)

        self._render_cketch(self.data.get('sketch_a_path'),
                            self.block_sketch_a_x,
                            self.block_sketch_a_y,
                            self.block_sketch_a_h)

        self._render_txt_block(self.block_txt1_x,
                               self.block_txt1_y,
                               TMPL_GATE,
                               self.data)

        self._render_txt_block(self.block_txt2_x,
                               self.block_txt2_y,
                               TMPL_FILL,
                               self.data)
        # self._renderCut()
        # attentions = self.data.get('attentions')
        # if attentions:
        #     self._renderAttentions(attentions)
        # beam_type = self.data.get('beam')
        # beam_length = self.data.get('beam_l')
        # self._renderBeamName(beam_type, beam_length)
        # self._renderBeam(self.data.get('beam'))
        # self._renderComments(self.data.get('comments'))

    def create_page_two(self):
        pass

    def renderImage(self, image_path, x, y, w=0, h=0):
            if image_path and os.path.exists(image_path):
                self.image(image_path, x=x, y=y, h=h, w=w)
            else:
                raise FileNotExistError(image_path)

    def _render_txt_block(self, x, y, tmpl, data, h=None, align='L'):
        if not h:
            h = self.textline_h
        self.set_xy(x, y)
        self.multi_cell(0,
                        h,
                        tmpl.format(**data),
                        align=align)

    def _renderCut(self):
        pass

    def _render_cketch(self, path, x, y, h):
        self.renderImage(path, x=x, y=y, h=h)

    def _renderAttentions(self, attentions):
        self.set_xy(self.block_attention_x, self.block_attention_y)
        self.set_text_color(210, 0, 0)  # red text color
        # FIXME only first value to print
        txt = 'ВНИМАНИЕ: ' + str(attentions[0])
        self.cell(0, self.textline_h, txt)
        self.set_text_color(0, 0, 0)  # black text color
