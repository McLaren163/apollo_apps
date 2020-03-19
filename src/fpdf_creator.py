import os
from fpdf import FPDF
from src import config as CFG
from src.exeptions import FileNotExistError

FONT_NAME = "STSEV"
FONT_FILE = CFG.FILES.get('font-stsev') 
FONT_SIZE = 14.0

LOGO_FILE = CFG.FILES.get('logo')

TXT_GATE = """Параметры проема:
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
  Цвет рамы: {frame_color} 
  Заполнение: {filling} 
  Цвет заполнения: {filling_color} 
  Структура краски: {color_type}"""

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

    block_gate_x = left_margin + 10
    block_gate_y = block_sketch_a_y + block_sketch_a_h + textline_h

    block_compl_x = left_margin
    block_compl_y = block_gate_y + textline_h * 7  # 6+1 rows in main block

    block_attention_x = left_margin
    block_attention_y = block_compl_y + textline_h * 8  # 7+1 rows in compl blc

    block_beamname_x = left_margin
    block_beamname_y = block_attention_y + textline_h * 2

    block_beam_x = block_beamname_x
    block_beam_y = block_beamname_y + textline_h
    block_beam_h = 40

    block_comments_x = block_beam_x
    block_comments_y = block_beam_y + block_beam_h + textline_h
    block_comments_w = 85

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

        self._render_cketch_a(self.data.get('sketch_a_path'))

        self._render_gate_text()
        # self._renderComplectation(self.data)
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

    def _render_gate_text(self):
        self.set_xy(self.block_gate_x, self.block_gate_y)
        self.multi_cell(0,
                        self.textline_h,
                        TXT_GATE.format(**self.data),
                        align='L')

    def _renderCut(self):
        pass

    def _renderComments(self, text):
        self.set_xy(self.block_comments_x, self.block_comments_y)
        # self.set_font('', 'B')
        self.cell(0, self.textline_h, 'ПРИМЕЧАНИЕ:', ln=2)
        self.multi_cell(self.block_comments_w,
                        self.textline_h,
                        text,
                        align='L')
        # self.set_font('', '')

    def _render_cketch_a(self, sketch_path):
        self.renderImage(sketch_path,
                         x=self.block_sketch_a_x,
                         y=self.block_sketch_a_y,
                         h=self.block_sketch_a_h)

    def _renderBeamName(self, beam_type, beam_length=0):
        txt = str(beam_type)
        if beam_length:
            txt = txt + ': ' + str(beam_length) + ' мм'

        self.set_xy(self.block_beamname_x, self.block_beamname_y)
        self.cell(0, self.textline_h, txt)

    def _renderBeam(self, beam_type):
        image_name = GATE_IMAGES['beams'].get(beam_type)
        self.renderImage(image_name,
                         x=self.block_beam_x,
                         y=self.block_beam_y,
                         h=self.block_beam_h)

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
