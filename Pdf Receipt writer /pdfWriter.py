from fpdf import FPDF 
from datetime import date 

class PDF(FPDF): 
    def draw_border(self): 
        '''Function that draws a rectangle around the receipt'''
        self.rect(5.0,5.0,200.0,287.0)
        self.rect(8.0,8.0,194.0,282.0)

    def set_document_date(self): 
        '''Function that writes the date on the document'''
        current_date = date.today()
        months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre'
        ,'Octubre','Noviembre','Diciembre']
        current_month = current_date.month
        current_day = current_date.day
        current_year = current_date.year
        text = 'Bogotá D.C, {month} {day} de {year}'.format(month=months[current_month-1], day=current_day, year=current_year)
        self.set_xy(30.0,20.0)
        self.cell(w=210.0,h=40.0,align='L',txt=text,border=0)

    def set_document_number(self,doc_num): 
        '''Function that writes the document number'''
        self.set_xy(128.0,20.0)
        text = 'CUENTA DE COBRO No. {doc_num}'.format(doc_num=doc_num)
        self.cell(w=210.0,h=40.0, txt=text, border=0)

    def set_recipient_info(self): 
        '''Function that writes the recipient information of the receipt'''
        self.set_font('Times','B',11)
        self.set_xy(10,75)
        text='Riesgo de Fractura S.A-NIT 830.027.158-3 \n    Dirección: Carrera 20B  No 74-46 \n  Teléfono: 7466400'
        self.multi_cell(0,5,text,align='C')
        self.set_font('Times','',11)
    
    def set_signature(self):
        '''Function that adds the image of the signature'''
        self.set_xy(30,205)
        self.image("Firma.png",w=75,h=25,link='',type='')

    def set_amount_text(self,amount_text):
        '''Function that adds the amount of the receipt in text format
        Inputs: 
        - amount_text: Text of the amount of the receipt
        '''
        self.set_font('Times','B',11)
        self.set_xy(0,160)
        self.cell(w=210,h=40,align='C',txt=amount_text)
        self.set_font('Times','',11)

    def draw_lines(self):
        '''Function that draws the lines around the total amount of the receipt'''
        self.set_line_width(0.0)
        self.dashed_line(160,150,190,150)
        self.line(160,157,190,157)
        self.line(160,158,190,158)

    def set_amount_values(self,amount_value): 
        '''Function that writes the the amount of the receipt and the total amount of the receipt
        in number format
        Inputs: 
         -amount_value: The amount of the receipt written in numbers
        '''
        self.set_xy(165,113)
        amount='$ {}'.format(amount_value)
        self.cell(w=210,h=40,txt=amount)
        self.set_xy(165,135)
        self.cell(w=210,h=40,txt=amount)
        self.draw_lines()
        
        
    def set_body(self): 
        '''Function that writes the body of the receipt'''
        self.set_xy(10,100)
        text1 ='DEBE A \n \n CRISTHIAN CAMILO SÁNCHEZ FINO'
        self.multi_cell(0,7,text1,align='C')

        text2 ='Distribución resultados participación U.T PROSUEÑO COLOMBIA \nsegún contrato por suministro equipos programa de atención integral\npacientes con apnea de sueño EPS-Sanitas'
        self.set_xy(30,130)
        self.multi_cell(0,5,text2,align='L')

        text3 ='TOTAL A PAGAR'
        self.set_xy(10,135)
        self.cell(w=210,h=40,align='C',txt=text3)       

        text4='Cordialmente,'
        self.set_xy(30,180)        
        self.cell(w=210,h=40,txt=text4)

        text5='CRISTHIAN CAMILO SÁNCHEZ FINO\nC.C  1.018.467.343 de Bogotá\nNIT 700.043.841-1\nBancolombia Cuenta Ahorros 205-257804-29'
        self.set_xy(30,230)        
        self.multi_cell(0,5,txt=text5)


    def set_document_layout(self): 
        '''Function that sets the general layout of the receipt'''
        self.set_font('Times','',11)
        self.set_text_color(0,0,0)
        self.set_document_date()
        self.set_recipient_info()
        self.set_body()
        self.set_signature()

    def set_document_values(self,doc_num,amount_text,amount_value):
        '''Function that sets the values of the receipt, the document number and the amount in text format
        Inputs: 
         -doc_num: The number of the document in text format 
         -amount_text: The amount of the receipt in text format
         -amount_value: The amount of the receipt in numbers
        '''
        self.set_document_number(doc_num)
        text = 'SON: {} PESOS MCTE**'.format(amount_text)
        self.set_amount_text(text)
        self.set_amount_values(amount_value)
