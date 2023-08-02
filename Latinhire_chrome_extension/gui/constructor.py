from tkinter import * 


def construct_gui(gui): 
    set_basic_params(gui)
    set_labels(gui)
    set_selectors(gui)
    set_buttons(gui)
    
def set_basic_params(gui):
    gui.title('Latinhire time tracker')     
    gui.geometry("750x500")
    gui.resizable(0,0)
    
def set_labels(gui):
    #Labels placement
    number_of_sessions = Label(gui,text='Number of sessions', fg='black',font='Verdana 18')
    number_of_sessions.place(x=0,y=50)
    gui.number_of_sessions = number_of_sessions
    number_of_missed_sessions = Label(gui,text='Missed sessions', fg='black',font='Verdana 18')
    number_of_missed_sessions.place(x=550,y=50)
    gui.number_of_missed_sessions = number_of_missed_sessions
    total_number_of_sessions = Label(gui, text=str(0), fg='black', font='Verdana 30')
    total_number_of_sessions.place(x=100,y=80)
    gui.total_number_of_sessions = total_number_of_sessions
    total_number_of_missed_sessions = Label(gui, text=str(0), fg='black', font='Verdana 30')
    total_number_of_missed_sessions.place(x=650,y=80)
    gui.total_number_of_missed_sessions = total_number_of_missed_sessions
    stopwatch = Label(gui, text=gui.string,fg='black',font='Verdana 40 bold')
    stopwatch.place(x=250,y=75)
    gui.stopwatch = stopwatch
    waiting_time = Label(gui, text='Waiting time',fg='black',font='Verdana 20')
    waiting_time.place(x=0,y=150)
    gui.waiting_time = waiting_time
    working_time = Label(gui, text='Working time',fg='black',font='Verdana 20')
    working_time.place(x=550,y=150)
    gui.working_time = working_time    
    current_session = Label(gui, text='Current session',fg='black',font='Verdana 20')
    current_session.place(x=250,y=150)
    current_session_time = Label(gui, text=gui.string, fg='black', font='Verdana 20')
    current_session_time.place(x=250,y=200)
    gui.current_session_time = current_session_time
    gui.current_session_time = current_session_time
    total_waiting_time = Label(gui, text=gui.string, fg='black', font='Verdana 20')
    total_waiting_time.place(x=0,y=200)
    gui.total_waiting_time = total_waiting_time
    total_working_time = Label(gui, text=gui.string, fg='black', font='Verdana 20')
    total_working_time.place(x=550,y=200)
    gui.total_working_time = total_working_time
    
    
def set_buttons(gui):
    #Buttons frame
    frame = Frame(gui)
    gui.start = Button(frame, text='Start shift',width=6,command = lambda:gui.start_shift('', gui.waiting_time),state='normal')
    gui.stop = Button(frame, text='End shift',width=6, command = gui.end_shift,state='disabled')
    gui.reset = Button(frame, text='Change',width=6, command = lambda:gui.change_status(''),state='disabled')
    frame.pack(anchor='center',pady=20)
    gui.start.pack(side='left')
    gui.stop.pack(side='right')
    gui.reset.pack(side='bottom')
    
    
def set_selectors(gui):
    #Language selector
    language_var = IntVar(gui,1)
    gui.language_var = language_var
    Label(gui, text='Language:', fg='black', font='Verdana 10 bold').place(x=375,y=250)
    Radiobutton(gui, text='Spanish', value=0, variable=language_var).place(x=460,y=250)
    Radiobutton(gui, text='English', value=1, variable=language_var).place(x=560,y=250)

    #Working hours selector
    Label(gui, text='Number of working hours:', fg='black', font='Verdana 10 bold').place(x=0,y=450)
    working_hours = [i for i in range(2,10,2)]
    working_hours_select_var = StringVar(gui) 
    working_hours_select_var.set(working_hours[0])
    gui.working_hours_select_var = working_hours_select_var
    
    working_hours_selector = OptionMenu(gui, working_hours_select_var, *working_hours)
    working_hours_selector.config(width=4, font=('Verdana',12))
    working_hours_selector.place(x=180,y=450)
    working_hours_select_var.trace("w", gui.update_working_hours)
    
    
    #Case selector 
    Label(gui, text='Case:', fg='black', font='Verdana 10 bold').place(x=0,y=250)
    cases = list(gui.text1Dict.keys())
    case_select_var = StringVar(gui)
    case_select_var.set(cases[0])
    gui.case_select_var = case_select_var

    options = OptionMenu(gui,case_select_var,*cases)
    options.config(width=28, font=('Verdana',12))
    options.place(x=50,y=250)

    texts_frame = Frame(gui)
    texts_frame.place(x=0,y=300)
    text1_title = Label(texts_frame, text='Text 1', font='Verdana 12 bold')
    text1_title.pack()
    text_field1 = Text(texts_frame,height=4,borderwidth=0,width=92)
    text_field1.insert(1.0,'')
    text_field1.pack()
    gui.text_field1 = text_field1
    text_field1.bind("<Button-1>",gui.copy_text_to_clipboard)

    text2_title = Label(texts_frame, text='Text 2', font='Verdana 12 bold')
    text2_title.pack()
    text_field2 = Text(texts_frame,height=4,borderwidth=0,width=92)
    text_field2.insert(1.0,'')
    text_field2.pack()
    text_field2.bind("<Button-1>",gui.copy_text_to_clipboard)
    gui.text_field2 = text_field2

    case_select_var.trace("w", gui.update_texts)
    language_var.trace("w", gui.update_texts)
    gui.update_texts()
    
    
    

    
    