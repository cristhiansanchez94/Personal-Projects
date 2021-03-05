from tkinter import *

#Detalles de la ventana 
mainWindow = Tk()
mainWindow.title('Generador de cuenta UT')
mainWindow.geometry("350x300")
mainWindow.resizable(0,0)

#Títulos 
Message(mainWindow, text='Generador de cuentas de cobro - UT',fg='black',font='Verdana 15 bold',width=200).place(x=30,y=0)
Label(mainWindow, text='Monto($):',fg='black',font='Verdana 10').place(x=25,y=100)
Label(mainWindow, text='Monto(texto):',fg='black',font='Verdana 10').place(x=25,y=150)
Label(mainWindow, text='Consecutivo:',fg='black',font='Verdana 10').place(x=25,y=200)
#Cuadros de texto 
quantity_num_text_field = Text(mainWindow,height=1,width=20).place(x=150,y=100)
quantity_text_text_field = Text(mainWindow,height=1,width=20).place(x=150,y=150)
receipt_number_text_field = Text(mainWindow,height=1,width=20).place(x=150,y=200)

#Botón
Button(mainWindow, text='Generar pdf',width=15, command = mainWindow.destroy).place(x=100,y=250)



mainWindow.mainloop() 