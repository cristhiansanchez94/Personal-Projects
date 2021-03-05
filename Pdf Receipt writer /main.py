from tkinter import *

#Detalles de la ventana 
mainWindow = Tk()
mainWindow.title('Generador de cuenta UT')
mainWindow.geometry("350x350")
mainWindow.resizable(0,0)

#Títulos 



#Cuadros de texto 


#Botón
Button(mainWindow, text='Generar pdf',width=15, command = mainWindow.destroy).place(x=100,y=300)
#Button(mainWindow, text='Generar pdf', width=10)


mainWindow.mainloop() 