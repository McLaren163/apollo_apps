import os
from fpdf import FPDF
from src.cfg.graphics import GATE_IMAGES
from .config import IMAGE_FOLDER

# font_name = 'DejaVu'
# font_file = './res/fonts/DejaVuSansCondensed.ttf'


class PDFShiftgate(FPDF):
    """ """
    textline_h = 6

    block_draft_x = 25
    block_draft_y = 35
    block_draft_h = 90

    block_beamname_x = 20
    block_beamname_y = 130
    block_beamname_w = 60

    block_beam_x = block_beamname_x
    block_beam_y = block_beamname_y + textline_h
    block_beam_w = block_beamname_w

    block_text_x = block_beam_x + block_beam_w + 5
    block_text_y = block_beamname_y

    def __init__(self, data, font=None):
        super().__init__()
        print('PDFShiftgate.__init__:', data)
        self.data = data
        if font:
            self.f_size = font.get('size') or 14
            try:
                self.add_font(font.get('name'), '', font.get('file'), uni=True)
                self.set_font(font.get('name'))
            except:
                pass

        self.l_margin = 20.0
        self.r_margin = 5.0
        self.t_margin = 5.0
        self.b_margin = 5.0

    def header(self):
        # Effective page width and height
        epw = self.w - self.l_margin - self.r_margin

        self.set_font_size(self.f_size)

        self.ln()
        self.cell(epw // 5, 10, 'Дата: ' + self.data.get('date'),
                  border=1, align='L')
        self.cell(0, 10,
                  'Откатные ворота ПРЕСТИЖ / ПРЕМИУМ (вид содвора)',
                  border=1, align='C')
        self.ln()
        self.cell(epw // 5, 10, 'Заказ: ' +
                  self.data.get('order'), border=1, align='L')
        self.cell(epw // 7 * 4, 10, 'Заказчик: ' +
                  self.data.get('customer'), border=1, align='L')
        self.cell(0, 10, 'Инженер: ' +
                  self.data.get('engineer'), border=1, align='L')

    def save(self, file):
        self.createOnePage()
        self.createTwoPage()
        self.output(file, 'F')

    def createOnePage(self):
        self.add_page('L')
        self.set_font_size(self.f_size - 2.0)

        self.renderDraft(self.data.get('draft_type'))

        # TODO render attention info

        self.renderBeamName(self.data.get('beam'), self.data.get('beam_l'))
        self.renderBeam(self.data.get('beam'))
        self.renderComplectation(self.data)
        self.renderComments(self.data.get('comments'))

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

    def renderComments(self, text):
        self.set_x(self.block_text_x)
        # self.set_font('', 'B')
        self.cell(0, self.textline_h, 'ПРИМЕЧАНИЕ:', ln=2)
        self.multi_cell(0, self.textline_h, text, align='L')
        # self.set_font('', '')

    def renderDraft(self, draft_type):
        image_name = GATE_IMAGES['draft_files'].get(draft_type)
        self.renderImage(image_name,
                         x=self.block_draft_x,
                         y=self.block_draft_y,
                         h=self.block_draft_h)

    def renderBeamName(self, beam_type, beam_length):
        txt = str(beam_type)
        if beam_length:
            txt = txt + ': ' + str(beam_length) + ' мм'

        self.set_xy(self.block_beamname_x, self.block_beamname_y)
        self.cell(self.block_beamname_w, self.textline_h, txt)

    def renderBeam(self, beam_type):
        image_name = GATE_IMAGES['beam_files'].get(beam_type)
        self.renderImage(image_name,
                         x=self.block_beam_x,
                         y=self.block_beam_y,
                         w=self.block_beam_w)

    def renderComplectation(self, data):
        self.set_xy(self.block_text_x, self.block_text_y)
        # self.set_font('', '')
        txt = """Рама: {frame} Цвет {frame_color} {color_type}
Заполнение: {filling} Цвет {filling_color}
Комплектация: {kit}
Столб приемный: {reception_column} {reception_column_height} мм {reception_column_num} шт
Столб от бокового качения: {console_column} {console_column_height} мм {console_column_num} шт
Зубчатая рейка: {rack} шт
Задвижка DH: {lock}"""
        self.multi_cell(0, self.textline_h, txt.format(**self.data), align='L')
