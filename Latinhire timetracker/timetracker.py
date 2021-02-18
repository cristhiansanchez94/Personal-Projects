from tkinter import * 
from datetime import datetime 
counter = 66600
running = False 
text1= 'HOLA AMIGUITO'
text2='TE AMO CARRITO'
def f1(label): 
    label['text'] = 'Start'
def f2(label): 
    label['text'] = 'Reset'
def f3(label): 
    label['text'] = 'Stop'
def copy_text_to_clipboard(event): 
    text = event.widget.get("1.0","end-1c")
    window.clipboard_clear()
    window.clipboard_append(text)

tt = datetime.fromtimestamp(counter)
string = tt.strftime("%H:%M:%S")
display = string 
#Parameters of the main window
window = Tk()
window.title('Latinhire time tracker')
window.geometry("750x500")
window.resizable(0,0)
#Buttons frame
frame = Frame(window)
start = Button(frame, text='Start shift',width=6,command = lambda:f1(label))
stop = Button(frame, text='End shift',width=6, command = lambda:f2(label))
reset = Button(frame, text='Change',width=6, command = lambda:f3(label2))
frame.pack(anchor='center',pady=20)
start.pack(side='left')
stop.pack(side='right')
reset.pack(side='bottom')

#Labels placement
stopwatch = Label(window, text=string,fg='black',font='Verdana 40 bold')
stopwatch.place(x=250,y=75)
waiting_time = Label(window, text='Waiting time',fg='black',font='Verdana 20')
waiting_time.place(x=0,y=150)
working_time = Label(window, text='Working time',fg='black',font='Verdana 20')
working_time.place(x=550,y=150)
total_waiting_time = Label(window, text=string, fg='black', font='Verdana 20')
total_waiting_time.place(x=0,y=200)
total_working_time = Label(window, text=string, fg='black', font='Verdana 20')
total_working_time.place(x=550,y=200)

language_var = IntVar(window,0)
Label(window, text='Language:', fg='black', font='Verdana 10 bold').place(x=375,y=250)
Radiobutton(window, text='Spanish', value=0, variable=language_var).place(x=460,y=250)
Radiobutton(window, text='English', value=1, variable=language_var).place(x=560,y=250)
#for i in range(1,4): 
#    Radiobutton(window, text='holi %i' %i, value=i, variable=var).pack()
#Button(window,text='holitas', command = lambda: print(var.get())).pack()
Label(window, text='Case:', fg='black', font='Verdana 10 bold').place(x=0,y=250)
cases = ['a','b','c']
case_select_var = StringVar(window)
case_select_var.set(cases[0])

options = OptionMenu(window,case_select_var,*cases)
options.config(width=28, font=('Verdana',12))
options.place(x=50,y=250)

texts_frame = Frame(window)
texts_frame.place(x=0,y=300)
text1_title = Label(texts_frame, text='Text 1', font='Verdana 12 bold')
text1_title.pack()
text_field1 = Text(texts_frame,height=4,borderwidth=0)
text_field1.insert(1.0,text1)
text_field1.pack()
text_field1.bind("<Button-1>",copy_text_to_clipboard)

text2_title = Label(texts_frame, text='Text 2', font='Verdana 12 bold')
text2_title.pack()
text_field2 = Text(texts_frame,height=4,borderwidth=0)
text_field2.insert(1.0,text2)
text_field2.pack()

text_field2.bind("<Button-1>",copy_text_to_clipboard)

window.mainloop()







