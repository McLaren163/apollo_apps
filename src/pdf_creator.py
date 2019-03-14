from fpdf import FPDF
from src.cfg.graphics import SGATE_IMG_CFG

# font_name = 'DejaVu'
# font_file = './res/fonts/DejaVuSansCondensed.ttf'

class PDFShiftgate(FPDF):
    """ """
    def __init__(self, data, font_name=None, font_file=None, font_size=14.0):
        super().__init__()
        self.data = data
        self.f_size = font_size
        if font_name and font_file:
            self.add_font(font_name, '', font_file, uni=True)
        if font_name:
            self.set_font(font_name)

    def header(self):
        l_margin = self.l_margin = 20.0
        r_margin = self.r_margin = 5.0
        t_margin = self.t_margin = 5.0
        b_margin = self.b_margin = 5.0

        # Effective page width and height
        epw = self.w - l_margin - r_margin

        self.set_font_size(self.f_size)

        self.ln()
        self.cell(epw // 5, 10, 'Дата: ' + self.data['date'],
            border=1, align='L')
        self.cell(0, 10,
            'Откатные ворота ПРЕСТИЖ / ПРЕМИУМ (вид содвора)', border=1, align='C')
        self.ln()
        self.cell(epw // 5, 10, 'Заказ: ' + self.data['order'], border=1, align='L')
        self.cell(epw // 7 * 4, 10, 'Заказчик: ' + self.data['customer'], border=1, align='L')
        self.cell(0, 10, 'Инженер: ' + self.data['engineer'], border=1, align='L')

    def save(self, file):
        self.createOnePage()
        self.createTwoPage()
        self.output(file, 'F')

    def createOnePage(self):
        self.add_page('L')
        file = SGATE_IMG_CFG['s_types'][self.data['s_type']]
        self.image(file, x=25, y=35, h=90)

    def createTwoPage(self):
        pass
