from tkinter import *
import pdfWriter 
import os 
import emailSender 
from datetime import date
current_directory = os.path.dirname(__file__)
email_recipients_directory = os.path.join(os.path.dirname(__file__),'email_recipients.txt')
email_credentials_path=os.path.join(os.path.dirname(__file__),'email_credentials.txt')
pdfTitle = ''
os.chdir(current_directory)


def create_pdf():
    '''Function that creates the receipt's pdf'''
    global pdfTitle
    amount_value= quantity_num_text_field.get("1.0","end-1c")
    amount_text = quantity_text_text_field.get("1.0","end-1c")
    doc_num = receipt_number_text_field.get("1.0","end-1c")
    pdf = pdfWriter.PDF()
    pdf.add_page()
    pdf.draw_border()
    pdf.set_document_layout()
    pdf.set_document_values(doc_num,amount_text,amount_value)
    months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    current_month =date.today().month -1-mode_var.get()
    current_year = date.today().year
    pdfTitle = 'Cuenta de Cobro UT {} {} - Cristhian Sánchez'.format(months[current_month],current_year)+'.pdf'
    try: 
        pdf.output(pdfTitle,'F')
        create_check_window()
    except: 
        post_message('Error while creating the pdf',error=True)
    

def get_recipients_emails(filepath):
    '''Function used to get the recipients emails from the filepath'''
    with open(filepath,'r') as reader: 
        text_content =reader.read()
    email_recipients,bcc_recipients = text_content.split('/')
    email_recipients = email_recipients.split(',') 
    bcc_recipients = bcc_recipients.split(',')
    return email_recipients, bcc_recipients

def send_email(): 
    '''Function that sends the email with a default message and the receipt attached to it'''
    global pdfTitle 
    email_recipients,bcc_recipients = get_recipients_emails(email_recipients_directory)
    attachment_location = pdfTitle
    try: 
        emailSender.EmailSender().send_email(email_recipients,pdfTitle[:-4], email_credentials_path,bcc_recipients,attachment_location=attachment_location)
        os.remove(pdfTitle)
        post_message('Email sent successfully')
    except: 
        post_message('Error sending the email',error=True)

def close_windows(): 
    '''Function to close all open windows from the exit window'''
    global mainWindow 
    mainWindow.destroy()

def create_check_window():
    '''Function used to create a window with the message to check the created pdf''' 
    global mainWindow 
    check_window = Toplevel(mainWindow)
    check_window.title('')
    check_window.geometry("450x100")
    check_window.resizable(0,0)
    Label(check_window, text='Pdf created successfully. Please check the file', fg='black', font='Verdana 12').place(x=40,y=20)
    Button(check_window, text='Send', width=10, command=send_email).place(x=70,y=60)
    Button(check_window, text='Close', width=10, command=check_window.destroy).place(x=270,y=60)

def post_message(message,error=False):
    '''Function used to create a window with a message
    Inputs: 
     - message: The message to be posted 
     - error: Indicator if the message is an error or a simple message 
    ''' 
    global mainWindow 
    message_window = Toplevel(mainWindow)
    message_window.title('')
    message_window.geometry("350x100")
    message_window.resizable(0,0)
    Label(message_window, text=message, fg='black', font='Verdana 12').place(x=40,y=20)
    if error: 
        Button(message_window, text='Ok', width=20, command=message_window.destroy).place(x=70,y=60)
    else: 
        Button(message_window, text='Ok', width=20, command=close_windows).place(x=70,y=60)

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


#Text fields 
quantity_num_text_field = Text(mainWindow,height=1,width=20)
quantity_num_text_field.place(x=150,y=100)
quantity_text_text_field = Text(mainWindow,height=1,width=20)
quantity_text_text_field.place(x=150,y=150)
receipt_number_text_field = Text(mainWindow,height=1,width=20)
receipt_number_text_field.place(x=150,y=200)

#Mode Selector 
mode_var = IntVar(mainWindow,1)
Label(mainWindow, text='Mes:',fg='black',font='Verdana 10').place(x=25,y=250)
Radiobutton(mainWindow, text='Actual', value=0, variable=mode_var).place(x=135,y=250)
Radiobutton(mainWindow, text='Anterior', value=1, variable=mode_var).place(x=235,y=250)

#Button
Button(mainWindow, text='Generar pdf',width=15, command = create_pdf).place(x=100,y=300)


mainWindow.mainloop() 