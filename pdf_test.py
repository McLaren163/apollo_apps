from fpdf import Template
from src.pdf_creator import PDFShiftgate

elements = [
    { 'name': 'box0', 'type': 'B', 'x1': 20.0, 'y1': 5.0,
        'x2': 205.0, 'y2': 292.0, 'font': None, 'size': 0.0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0,
        'align': 'I', 'text': None, 'priority': 2, },
    { 'name': 'box1', 'type': 'B', 'x1': 100.0, 'y1': 272.0,
        'x2': 205.0, 'y2': 292.0, 'font': None, 'size': 0.0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0,
        'align': 'I', 'text': None, 'priority': 2, },
    { 'name': 'company_logo', 'type': 'I', 'x1': 186.0, 'y1': 273.0,
        'x2': 204.0, 'y2': 291.0, 'font': None, 'size': 0.0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0,
        'align': 'C', 'text': './res/img/123.jpg', 'priority': 0, },
    { 'name': 'txt', 'type': 'T', 'x1': 100.0, 'y1': 50.0,
        'x2': 150.0, 'y2': 200.0, 'font': 'DejaVu', 'size': 16.0, 'bold': 0,
        'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0,
        'align': 'C', 'text': 'Проверочный текст', 'priority': 0, },
]
# f = Template(format="A4", elements=elements,
#              title="Sample Invoice")
# f.add_page()
# f.pdf.add_font('DejaVu', '', './res/fonts/DejaVuSansCondensed.ttf', uni=True)
# f.pdf.set_font('DejaVu', '', 14)
# # f["company_name"] = "Sample Company"
# # f["company_logo"] = "./res/img/123.jpg"
# f.render("./template.pdf")

font_name = 'DejaVu'
font_file = './res/fonts/DejaVuSansCondensed.ttf'
# font_file = './res/fonts/calibri.ttf'

data = {
    'order': '99',
    'customer': 'Иванов Петр Иванович'
}

pdf = PDFShiftgate(data, font_name, font_file, 14.0)
pdf.save('template.pdf')

