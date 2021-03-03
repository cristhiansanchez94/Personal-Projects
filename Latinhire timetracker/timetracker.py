from tkinter import * 
from datetime import datetime, date 
import time 
import DataWriter

general_counter = 18000
waiting_counter = 18000
working_counter = 18000
running = False 
text1Dict = {
'End session':'If you don’t need further explanation on this question, we can end the session. I’d really appreciate you letting me know how I did by rating our session after you exit. Thanks and have a great day!',
'Cheating': 'Before we start, may I ask, is this from a graded test, quiz, or timed assessment?',
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
text1Dict_spa= {
'End session':'Si no necesitas que explique más a profundidad en esta pregunta, podemos terminar la sesión. Realmente apreciaría si me dejas saber cómo lo hice al calificar nuestra sesión una vez termine. ¡Gracias y ten un buen día!',
'Cheating': 'Antes de comenzar, puedo preguntar, ¿es esto de un quiz, examen calificado o una evaluación con tiempo?',
'Off-Topic': 'Por favor recuerda que la tutoría es para preguntas académicas únicamente. ¿Eres capaz de enfocarte en aprender?',
'Offensive Language': 'Maldecir y el lenguaje ofensivo son una violación de nuestra guía comunitaria y no está permitido en Brainly. Por favor abstente de usar lenguaje irrespestuoso o tendré que terminar nuestra sesión.',
'Disrespectful':'Este tipo de comportamiento irrespetuoso is una violación de la guía comunitaria de Brainly. Si no puedes comportarte respetuosamente conmigo, no podré continuar nuestra sesión.',
'Sexual Content':'Brainly es un espacio seguro para que los estudiantes puedan recibir la ayuda que necesitan con su tarea y trabajos de la escuela. Voy a terminar y reportar esta sesión por violar nuestra guía comunitaria.',
'User Needs Help':'Sólo quería recordarte que Brainly es para objetivos educacionales únicamente - ¿Eres capaz de enfocarte en aprender?',
'Violent Threats':'Brainly tiene una política de tolerancia cero para la violencia y las amenazas en nuestra plataforma. Voy a terminar y reportar esta sesión para una revisión posterior de seguridad.',
'Illegal Activiy':'Brainly es un espacio seguro para que los estudiantes puedan recibir la ayuda que necesitan con su tarea y trabajos de la escuela. Voy a terminar y reportar esta sesión  para una revisión posterior de seguridad.',
'Wrong subject':'Lo siento, pero no podré ayudarte con esta pregunta porque (soy un tutor de matemáticas / es muy compleja), depronto ¿quisieras publicarla en Brainly.com?',
'Not knowing the answer':'Lo siento, pero no podré ayudar con esta pregunta porque está fuera de mi área de experticia. Depronto ¿quisieras preguntarle a otro tutor o publicarla en Brainly.com?'
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
text2Dict_spa = {
'End session':'Sólo quería confirmar que mi explicación fue clara. Si todavía estás ahí por favor déjamelo saber en el chat, de lo contrario, daré por terminada la sesión. Realmente apreciaría si me dejas saber cómo me fue en la sesión calificándome al finalizar la sesión. Gracias y ¡ten un gran día!',
'Cheating':'Desafortunadamente no puedo ayudarte ya que esto parece ser un quiz, examen o una evaluación y es una violación de la guía comunitaria de Brainly. Por favor revisa nuestro código de honor antes de solicitar una tutoría en el futuro: https://brainly.com/honor-code. Ten en cuenta que si intentas usar Brainly para hacer trampa de nuevo, se tomarán acciones respecto a tu cuenta.',
'Off-Topic':'Has roto repetidamente nuestra guía comunitara, por lo que voy a terminar y reportar la sesión. Por favor revisa nuestra guía comunitaria aquí  brainly.com/community-guidelines antes de solicitar una tutoría en el futuro.',
'Offensive Language':'Voy a terminar y reportar la sesión ahora porque has violado repetidamente nuestra guía comunitaria. Por favor revísala en brainly.com/community-guidelines antes de usar las tutorías de Brainly nuevamente.',
'Disrespectful':'Voy a terminar y reportar la sesión ahora porque has violado repetidamente nuestra guía comunitaria. Por favor revísala en brainly.com/community-guidelines antes de usar las tutorías de Brainly nuevamente.',
'Sexual Content':'',
'User Needs Help':'Lamento que te sientas de esa forma. Te recomiendo que hables con un adulto de confianza sobre cómo te sientes. No estás solo, y hay ayuda muy útil en la línea de crisis http://www.crisistextline.org/ y la línea nacional de prevención del suicidio (1-800-273-TALK) con quién tú puedes hablar confidencialmente. Debo terminar nuestra sesión, pero un miembro del equipo de Brainly hará seguimiento contigo más tarde en el día para asegurarse de que estás bien.',
'Violent Threats':'',
'Illegal Activiy':'',
'Wrong subject':'',
'Not knowing the answer':''
}

current_status='waiting'
running=False 

def change_time_label(label,counter):
    '''Function that updates a label timestamp with a counter 
    Inputs: 
    -label: The label to be updated 
    -counter: The counter used to update the label
    '''
    tt=datetime.fromtimestamp(counter)
    string = tt.strftime("%H:%M:%S")
    display = string
    label['text']=display

def time_tracker(): 
    '''Function that runs the time_tracker'''
    def count(): 
        if running: 
            global general_counter 
            global waiting_counter
            global working_counter
            if general_counter ==18000: 
                stopwatch.after(1000,count)
                display = 'Starting'
                stopwatch['text']=display
                general_counter+=1
                waiting_counter+=1                                
            else:         
                stopwatch.after(1000,count)
                change_time_label(stopwatch,general_counter)                
                general_counter+=1
                if current_status=='waiting':
                    change_time_label(total_waiting_time,waiting_counter)
                    waiting_counter+=1
                else: 
                    change_time_label(total_working_time,working_counter)
                    working_counter+=1
    count()

def StartShift(label): 
    '''Activation function of the 'Start shift' button'''
    global running 
    running = True 
    start['state']='disabled'
    stop['state']='normal'
    reset['state']='normal'
    time_tracker()
    label['font'] = 'Verdana 19 bold'
    
def ChangeStatus(): 
    '''Activation function of the 'Change' button'''
    global current_status 
    global working_counter
    global waiting_counter
    if current_status =='waiting': 
        current_status = 'working'
        working_time['font']='Verdana 19 bold'
        waiting_time['font']='Verdana 20'
        working_counter+=1
    else: 
        current_status = 'waiting'
        waiting_time['font']='Verdana 19 bold'
        working_time['font']='Verdana 20'
def EndShift(): 
    '''Activation function of the 'End Shift' button'''
    global running 
    global waiting_counter
    global working_counter
    global window 
    reset['state']='disabled'
    stop['state']='disabled'
    running = False
    window.quit()
    exit_window = create_exit_window()
    working_minutes = str(max(round(calculate_minutes(working_counter),2),0))
    waiting_minutes = str(max(round(calculate_minutes(waiting_counter),2),0))
    Label(exit_window,text=waiting_minutes, fg='black', font='Verdana 13').place(x=300,y=50)
    Label(exit_window,text=working_minutes, fg='black', font='Verdana 13').place(x=300,y=100)
    exit_window.mainloop()

def calculate_minutes(counter): 
    '''Function that calculates the total amount of time, in minutes, from the counter
    Inputs: 
     -counter: counter to be used to calculate the minutes of the timestamp
    Outputs: 
     -time_in_minutes: the total amount of minutes of the timestamp represented by counter
    '''
    dt = datetime.fromtimestamp(counter)
    time_in_minutes = dt.hour*60 + dt.minute + (dt.second-1)/60
    return time_in_minutes

def write_data_to_gdrive(folder_text_field,file_text_field): 
    '''Function used to save the results to google drive
    Inputs: 
     - folder_text_field: The text field that contains the folder name 
     - file_text_field: The text fiedl that contains the file name
    '''
    global waiting_counter
    global working_counter
    FolderTitle=folder_text_field.get("1.0","end-1c")
    SheetTitle= file_text_field.get("1.0","end-1c")
    working_minutes = str(max(round(calculate_minutes(working_counter),2),0)).replace(".",",")
    waiting_minutes = str(max(round(calculate_minutes(waiting_counter),2),0)).replace(".",",")
    try: 
        DataWriter.DataWriter().writeData(SheetTitle,FolderTitle,waiting_minutes,working_minutes)
        post_message('Data saved successfully')
    except: 
        post_message('There has been an error while saving',error=True)

def post_message(message,error=False):
    '''Function used to create a window with a message
    Inputs: 
     - message: The message to be posted 
     - error: Indicator if the message is an error o a simple message 
    ''' 
    global window 
    message_window = Toplevel(window)
    message_window.title('')
    message_window.geometry("350x100")
    message_window.resizable(0,0)
    Label(message_window, text=message, fg='black', font='Verdana 12').place(x=40,y=20)
    if error: 
        Button(message_window, text='Ok', width=20, command=message_window.destroy).place(x=70,y=60)
    else: 
        Button(message_window, text='Ok', width=20, command=close_windows).place(x=70,y=60)


def update_texts(*args):
    '''
    Function that updates the text boxes according to the selected options in the language and case selectors
    '''
    dictKey = case_select_var.get()
    language_selector = language_var.get()
    if language_selector==1: 
        text_field1_value = text1Dict.get(dictKey)
        text_field1.delete('1.0',END)
        text_field1.insert(1.0,text_field1_value)
        text_field2_value = text2Dict.get(dictKey)
        text_field2.delete('1.0',END)
        text_field2.insert(1.0,text_field2_value)
    else: 
        text_field1_value = text1Dict_spa.get(dictKey)
        text_field1.delete('1.0',END)
        text_field1.insert(1.0,text_field1_value)
        text_field2_value = text2Dict_spa.get(dictKey)
        text_field2.delete('1.0',END)
        text_field2.insert(1.0,text_field2_value)

    

def copy_text_to_clipboard(event): 
    '''Function to copy the clicked text box to the clipboard'''
    text = event.widget.get("1.0","end-1c")
    window.clipboard_clear()
    window.clipboard_append(text)

def close_windows(): 
    '''Function to close all open windows from the exit window'''
    global window 
    window.destroy()

def create_exit_window(): 
    '''Function that creates the window once the 'End Shift' button is activated
    Outputs: 
     - exit_window: The object of the created window
    '''
    global window
    exit_window = Toplevel(window)
    exit_window.title('')
    exit_window.geometry("400x250")
    exit_window.resizable(0,0)
    Label(exit_window, text='Shift is over!',fg='black',font='Verdana 20 bold').pack()
    Label(exit_window, text='Total waiting minutes: ', fg='black', font='Verdana 15 bold').place(x=0,y=50)
    Label(exit_window, text='Total working minutes: ', fg='black', font='Verdana 15 bold').place(x=0,y=100)
    Label(exit_window, text='Would you like to save this results? ', fg='black', font='Verdana 13').place(x=50,y=150)
    Button(exit_window, text='Yes',width=10,command=create_saving_window).place(x=40,y=200)
    Button(exit_window, text='No',width=10,command=close_windows).place(x=250,y=200)
    return exit_window

def create_saving_window(): 
    '''Function that creates the window once the 'Yes' button is activated at the exit_window
    Outputs: 
     - saving_window: The object of the created window
    '''
    global window
    saving_window = Toplevel(window)
    saving_window.title('')
    saving_window.geometry("400x250")
    saving_window.resizable(0,0)
    Message(saving_window, text='Save in google drive: select the desired location(use the same file name everytime)',fg='black',font='Verdana 10 ',width=300).pack()
    Label(saving_window, text='Folder name: ', fg='black', font='Verdana 15 bold').place(x=0,y=50)
    Label(saving_window, text='File name: ', fg='black', font='Verdana 15 bold').place(x=0,y=100)
    folder_name_text_field = Text(saving_window,height=1,borderwidth=0,width=20)
    folder_name_text_field.place(x=155,y=50)
    folder_name_text_field.insert(1.0,'')
    file_name_text_field = Text(saving_window,height=1,borderwidth=0,width=30)
    file_name = 'Latinhire time tracker ' + str(date.today().year)
    file_name_text_field.insert(1.0,file_name)
    file_name_text_field.place(x=125,y=100)
    Button(saving_window, text='Save',width=20,command = lambda : write_data_to_gdrive(folder_name_text_field,file_name_text_field)).place(x=100,y=150)    

#Section of the main window 
tt = datetime.fromtimestamp(general_counter)
string = tt.strftime("%H:%M:%S")
display = string 
#Parameters of the main window
window = Tk()
window.title('Latinhire time tracker')
window.geometry("750x500")
window.resizable(0,0)
#Buttons frame
frame = Frame(window)
start = Button(frame, text='Start shift',width=6,command = lambda:StartShift(waiting_time),state='normal')
stop = Button(frame, text='End shift',width=6, command = EndShift,state='disabled')
reset = Button(frame, text='Change',width=6, command = ChangeStatus,state='disabled')
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
language_var = IntVar(window,1)
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








