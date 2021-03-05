from fpdf import FPDF 
from datetime import date 

class PDF(FPDF): 
    def draw_border(self): 
        self.rect(5.0,5.0,200.0,287.0)
        self.rect(8.0,8.0,194.0,282.0)

    def set_document_date(self): 
        current_date = date.today()
        months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre'
        ,'Octubre','Noviembre','Diciembre']
        current_month = current_date.month
        current_day = current_date.day
        current_year = current_date.year
        text = 'Bogotá D.C {month} {day} de {year}'.format(month=months[current_month-1], day=current_day, year=current_year)
        self.set_xy(30.0,20.0)
        self.cell(w=210.0,h=40.0,align='L',txt=text,border=0)

    def set_document_number(self,doc_num): 
        self.set_xy(128.0,20.0)
        text = 'CUENTA DE COBRO No. {doc_num}'.format(doc_num=doc_num)
        self.cell(w=210.0,h=40.0, txt=text, border=0)

    def set_document_layout(self): 
        self.set_font('Times','',11)
        self.set_text_color(0,0,0)
        self.set_document_date()
        self.set_document_number('0004')

pdf = PDF()
pdf.add_page()
#pdf_w = 210
#pdf_h = 297
#pdf.draw_border()
pdf.set_document_layout()
pdf.output('prueba.pdf','F')