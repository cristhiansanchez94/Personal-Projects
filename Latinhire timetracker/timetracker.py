from tkinter import * 
from datetime import datetime 
counter = 18000
running = False 
text1Dict = {
'End session':'If you don’t need further explanation on this question, we can end the session. I’d really appreciate you letting me know how I did by rating our session after you exit. Thanks and have a great day!',
'Cheating': 'Is this from a graded test, quiz, or timed assessment?',
'Off-Topic': 'Please remember that tutoring is for academic questions only. Are you able to stay focused on learning?',
'Offensive Language': 'Cursing and offensive language is a violation of our Community Guidelines and not allowed on Brainly. Please refrain from using disrespectful language like this or I’ll have to end our session.',
'Disrespectful':'This sort of disrespectful behavior is a violation of Brainly’s Community Guidelines. If you can’t behave respectfully towards me, I won’t be able to continue our session.',
'Sexual Content':'Brainly is intended to be a safe place for students to get the help they need with their homework and school assignments. I’ll be ending and reporting this session for violating our Community Guidelines.',
'User Needs Help':'Just wanted to remind you that Brainly is intended for educational purposes only - are you able to continue staying focused on learning?',
'Violent Threats':'Brainly has a zero-tolerance policy for violence and threats on our platform. I’ll be ending and reporting this session for a further safety review.',
'Illegal Activiy':'Brainly is intended to be a safe place for students to get the help they need with their homework and school assignments. I’ll be ending and reporting this session for a further safety review.',
'Wrong subject':'I am sorry, but I won\'t be able to help you with that question because (it is not in English/ I am a Math tutor/ it is too complex), perhaps you would like to post it on Brainly.com?',
'Not knowing the answer':'I am sorry, but I won\'t be able to help you with that question because it is outside of my expertise. Perhaps you would like to ask a different tutor or post it on Brainly.com?'
}
text2Dict = {
'End session':'I just wanted to double-check that my explanation was clear -if you\'re still there please let me know in the chat, otherwise I\'ll go ahead and wrap up our session. I\'d really appreciate you letting me know how I did by rating our session after you exit. Thanks and have a great day!',
'Cheating':'Unfortunately, I can’t help you as this appears to be a quiz, test, or assessment, and is a violation of Brainly’s Community Guidelines. Please review our Honor Code prior to requesting tutoring in the future: https://brainly.com/honor-code. Keep in mind that if you attempt to use Brainly to cheat again, further action may be taken on your account.',
'Off-Topic':'You’ve repeatedly broken our community guidelines, so I’ll be ending and reporting this session now. Please review our community guidelines here brainly.com/community-guidelines before requesting Brainly Tutoring in the future.',
'Offensive Language':'I’ll be ending and reporting this session now because you’ve repeatedly violated our guidelines. Please review them at brainly.com/community-guidelines before using Brainly tutoring again.',
'Disrespectful':'I’ll be ending and reporting this session now because you’ve repeatedly violated our guidelines. Please review them at brainly.com/community-guidelines prior to using Brainly tutoring again.',
'Sexual Content':'',
'User Needs Help':'I’m so sorry you’re feeling this way and strongly recommend that you talk to a parent or trusted adult about how you\'re feeling. You’re not alone, and there are some really helpful people at the Crisis Text Line http://www.crisistextline.org/ and the National Suicide Prevention Hotline (1-800-273-TALK) whom you can talk to confidentially. I have to end our session now, but a Brainly team member will be following up with you later today to make sure you’re doing okay.',
'Violent Threats':'',
'Illegal Activiy':'',
'Wrong subject':'',
'Not knowing the answer':''
}
current_status='waiting'
def StartShift(label): 
    label['font'] = 'Verdana 19 bold'
def ChangeStatus(): 
    global current_status 
    if current_status =='waiting': 
        current_status = 'working'
        working_time['font']='Verdana 19 bold'
        waiting_time['font']='Verdana 20'
    else: 
        current_status = 'waiting'
        waiting_time['font']='Verdana 19 bold'
        working_time['font']='Verdana 20'
def EndShift(label): 
    label['text'] = 'Stop'

def update_texts(*args):
    dictKey = case_select_var.get()
    text_field1_value = text1Dict.get(dictKey)
    text_field1.delete('1.0',END)
    text_field1.insert(1.0,text_field1_value)
    text_field2_value = text2Dict.get(dictKey)
    text_field2.delete('1.0',END)
    text_field2.insert(1.0,text_field2_value)

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
start = Button(frame, text='Start shift',width=6,command = lambda:StartShift(waiting_time))
stop = Button(frame, text='End shift',width=6, command = lambda:EndShift(working_time))
reset = Button(frame, text='Change',width=6, command = ChangeStatus)
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

#Language selector
language_var = IntVar(window,0)
Label(window, text='Language:', fg='black', font='Verdana 10 bold').place(x=375,y=250)
Radiobutton(window, text='Spanish', value=0, variable=language_var).place(x=460,y=250)
Radiobutton(window, text='English', value=1, variable=language_var).place(x=560,y=250)

#Case selector 
Label(window, text='Case:', fg='black', font='Verdana 10 bold').place(x=0,y=250)
cases = list(text1Dict.keys())
case_select_var = StringVar(window)
case_select_var.set(cases[0])

options = OptionMenu(window,case_select_var,*cases)
options.config(width=28, font=('Verdana',12))
options.place(x=50,y=250)

texts_frame = Frame(window)
texts_frame.place(x=0,y=300)
text1_title = Label(texts_frame, text='Text 1', font='Verdana 12 bold')
text1_title.pack()
text_field1 = Text(texts_frame,height=4,borderwidth=0,width=92)
text_field1.insert(1.0,'')
text_field1.pack()
text_field1.bind("<Button-1>",copy_text_to_clipboard)

text2_title = Label(texts_frame, text='Text 2', font='Verdana 12 bold')
text2_title.pack()
text_field2 = Text(texts_frame,height=4,borderwidth=0,width=92)
text_field2.insert(1.0,'')

text_field2.pack()

text_field2.bind("<Button-1>",copy_text_to_clipboard)

case_select_var.trace("w", update_texts)
language_var.trace("w", update_texts)
update_texts()


window.mainloop()







