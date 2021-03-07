from tkinter import *
import pdfWriter 

def create_pdf():
    '''Function that creates the receipt's pdf'''
    amount_value= quantity_num_text_field.get("1.0","end-1c")
    amount_text = quantity_text_text_field.get("1.0","end-1c")
    doc_num = receipt_number_text_field.get("1.0","end-1c")
    pdf = pdfWriter.PDF()
    pdf.add_page()
    pdf.draw_border()
    pdf.set_document_layout()
    pdf.set_document_values(doc_num,amount_text,amount_value)
    pdf.output('output.pdf','F')


#Window details
mainWindow = Tk()
mainWindow.title('Generador de cuenta UT')
mainWindow.geometry("350x350")
mainWindow.resizable(0,0)

#Titles 
Message(mainWindow, text='Generador de cuentas de cobro - UT',fg='black',font='Verdana 15 bold',width=200).place(x=30,y=0)
Label(mainWindow, text='Monto($):',fg='black',font='Verdana 10').place(x=25,y=100)
Label(mainWindow, text='Monto(texto):',fg='black',font='Verdana 10').place(x=25,y=150)
Label(mainWindow, text='Consecutivo:',fg='black',font='Verdana 10').place(x=25,y=200)
Label(mainWindow, text='Ruta:',fg='black',font='Verdana 10').place(x=25,y=250)
#Text fields 
quantity_num_text_field = Text(mainWindow,height=1,width=20)
quantity_num_text_field.place(x=150,y=100)
quantity_text_text_field = Text(mainWindow,height=1,width=20)
quantity_text_text_field.place(x=150,y=150)
receipt_number_text_field = Text(mainWindow,height=1,width=20)
receipt_number_text_field.place(x=150,y=200)

#Button
Button(mainWindow, text='Generar pdf',width=15, command = create_pdf).place(x=100,y=300)


mainWindow.mainloop() 