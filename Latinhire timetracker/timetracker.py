from tkinter import * 
from datetime import datetime 
counter = 66600
running = False 

def f1(label): 
    label['text'] = 'Start'
def f2(label): 
    label['text'] = 'Reset'
def f3(label): 
    label['text'] = 'Stop'

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

var = IntVar(window,0)
for i in range(1,4): 
    Radiobutton(window, text='holi %i' %i, value=i, variable=var).pack()
Button(window,text='holitas', command = lambda: print(var.get())).pack()
window.mainloop()







