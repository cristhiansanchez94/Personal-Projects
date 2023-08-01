from tkinter import * 
from datetime import datetime, date
from .utils import calculate_minutes, change_time_label
from .constructor import construct_gui
from .dictionaries import text1Dict, text1Dict_spa, text2Dict, text2Dict_spa
import DataWriter
import traceback 

COUNTER = -3600

class Gui(Tk):
    def __init__(self):
        super().__init__()
        
        self.counter = COUNTER  
        self.general_counter = COUNTER
        self.waiting_counter = COUNTER
        self.working_counter = COUNTER
        self.current_session_counter = COUNTER   
        self.running = False  
        self.num_sessions = 0
        self.num_missed_sessions = 0
        
        self.text1Dict = text1Dict 
        self.text1Dict_spa = text1Dict_spa 
        self.text2Dict = text2Dict 
        self.text2Dict_spa = text2Dict_spa 
        
        tt = datetime.fromtimestamp(self.general_counter)
        self.string = tt.strftime("%H:%M:%S")
        self.display = self.string 
        construct_gui(self)
        
        self.current_status = 'waiting'
        self.bind("<<StatusChanged>>", self.change_status)
        self.bind("<<StartShift>>", lambda event: self.start_shift(event,self.waiting_time))
        self.bind("<<EndShift>>", self.end_shift)
        self.bind("<<EndShiftUnexp>>", self.end_shift_unexpected)
        self.bind("<<MissedSession>>", self.register_missed_session)
        
    def register_missed_session(self, event=''):
        self.num_missed_sessions+=1
        self.post_message('You just missed a session!. Pay attention', alert=True)
        self.total_number_of_missed_sessions['text'] = str(self.num_missed_sessions)
        
    def write_data_to_gdrive(self, folder_text_field,file_text_field): 
        '''Function used to save the results to google drive
        Inputs: 
        - folder_text_field: The text field that contains the folder name 
        - file_text_field: The text field that contains the file name
        '''
        FolderTitle=folder_text_field.get("1.0","end-1c")
        SheetTitle= file_text_field.get("1.0","end-1c")
        working_minutes = calculate_minutes(self.working_counter)
        waiting_minutes = calculate_minutes(self.waiting_counter)
        try: 
            DataWriter.DataWriter().writeData(SheetTitle,FolderTitle,waiting_minutes,working_minutes,self.num_sessions)
            self.post_message('Data saved successfully')
        except Exception as e: 
            print(traceback.format_exc())
            self.post_message('There has been an error while saving',error=True)
        
    def create_saving_window(self): 
        '''Function that creates the window once the 'Yes' button is activated at the exit_window
        Outputs: 
        - saving_window: The object of the created window
        '''
        saving_window = Toplevel(self)
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
        Button(saving_window, text='Save',width=20,command = lambda : self.write_data_to_gdrive(folder_name_text_field,file_name_text_field)).place(x=100,y=150)    
    
        
    def create_exit_window(self): 
        '''Function that creates the window once the 'End Shift' button is activated
        Outputs: 
            - exit_window: The object of the created window
        '''
        exit_window = Toplevel(self)
        exit_window.title('')
        exit_window.geometry("400x300")
        exit_window.resizable(0,0)
        Label(exit_window, text='Shift is over!',fg='black',font='Verdana 20 bold').pack()
        Label(exit_window, text='Total waiting minutes: ', fg='black', font='Verdana 15 bold').place(x=0,y=50)
        Label(exit_window, text='Total working minutes: ', fg='black', font='Verdana 15 bold').place(x=0,y=100)
        Label(exit_window, text='Number of sessions: ', fg='black', font='Verdana 15 bold').place(x=0,y=150)
        Label(exit_window, text='Would you like to save this results? ', fg='black', font='Verdana 13').place(x=50,y=200)
        Button(exit_window, text='Yes',width=10,command=self.create_saving_window).place(x=40,y=250)
        Button(exit_window, text='No',width=10,command=self.close_windows).place(x=250,y=250)
        return exit_window
        
    def close_windows(self): 
        '''Function to close all open windows from the exit window'''
        self.destroy()
        
    def end_shift_unexpected(self, event=''):
        self.post_message('End shift signal was received unexpectedly. The shift is not over!', alert=True)
    
    def post_message(self, message,error=False, alert = False):
        '''Function used to create a window with a message
        Inputs: 
        - message: The message to be posted 
        - error: Indicator if the message is an error o a simple message 
        ''' 
        message_window = Toplevel(self)
        message_window.title('')
        message_window.geometry("350x100")
        message_window.resizable(0,0)
        Label(message_window, text=message, fg='black', font='Verdana 12').place(x=40,y=20)
        if error or alert: 
            Button(message_window, text='Ok', width=20, command=message_window.destroy).place(x=70,y=60)
        else: 
            Button(message_window, text='Ok', width=20, command=self.close_windows).place(x=70,y=60)
        
    def time_tracker(self): 
        '''Function that runs the time_tracker'''
        def count(): 
            if self.running: 
                if self.general_counter ==COUNTER: 
                    self.stopwatch.after(1000,count)
                    display = 'Starting'
                    self.stopwatch['text']=display
                    self.general_counter+=1
                    self.waiting_counter+=1                                
                else:         
                    self.stopwatch.after(1000,count)
                    change_time_label(self.stopwatch,self.general_counter)                
                    self.general_counter+=1
                    if self.current_status=='waiting':
                        change_time_label(self.total_waiting_time,self.waiting_counter)
                        self.waiting_counter+=1
                    else: 
                        change_time_label(self.total_working_time,self.working_counter)
                        self.working_counter+=1
                        change_time_label(self.current_session_time,self.current_session_counter)
                        self.current_session_counter+=1
                        if self.current_session_counter==COUNTER + 900: 
                            self.post_message("15 min already",alert=True)
        count()
    
    def start_shift(self,event='',label=''): 
        '''Activation function of the 'Start shift' button'''
        self.running = True 
        self.start['state']='disabled'
        self.stop['state']='normal'
        self.reset['state']='normal'
        self.time_tracker()
        label['font'] = 'Verdana 19 bold'
        
    def change_status(self, event=''): 
        '''Activation function of the 'Change' button'''
        if self.current_status =='waiting': 
            self.current_status = 'working'
            self.working_time['font']='Verdana 19 bold'
            self.waiting_time['font']='Verdana 20'
            self.num_sessions +=1
            self.total_number_of_sessions['text'] = str(self.num_sessions)
        else: 
            self.current_status = 'waiting'
            self.current_session_counter = COUNTER
            change_time_label(self.current_session_time,self.current_session_counter)
            self.waiting_time['font']='Verdana 19 bold'
            self.working_time['font']='Verdana 20'
        
    def end_shift(self,event=''): 
        '''Activation function of the 'End Shift' button'''
        
        self.reset['state']='disabled'
        self.stop['state']='disabled'
        self.running = False
        self.quit()
        exit_window = self.create_exit_window()
        delta_counter = (self.general_counter -COUNTER)  - ((self.working_counter - COUNTER)+(self.waiting_counter - COUNTER))
        self.working_counter +=delta_counter
        change_time_label(self.total_working_time,self.working_counter)
        change_time_label(self.total_waiting_time,self.waiting_counter)
        change_time_label(self.stopwatch,self.general_counter)
        working_minutes = str(round(calculate_minutes(self.working_counter),2))
        waiting_minutes = str(round(calculate_minutes(self.waiting_counter),2))
        Label(exit_window,text=waiting_minutes, fg='black', font='Verdana 13').place(x=300,y=50)
        Label(exit_window,text=working_minutes, fg='black', font='Verdana 13').place(x=300,y=100)
        Label(exit_window,text=self.num_sessions, fg='black', font='Verdana 13').place(x=300,y=150)
        exit_window.mainloop()
        
    def update_texts(self, *args):
        '''
        Function that updates the text boxes according to the selected options in the language and case selectors
        '''
        dictKey = self.case_select_var.get()
        language_selector = self.language_var.get()
        if language_selector==1: 
            text_field1_value = text1Dict.get(dictKey)
            self.text_field1.delete('1.0',END)
            self.text_field1.insert(1.0,text_field1_value)
            text_field2_value = text2Dict.get(dictKey)
            self.text_field2.delete('1.0',END)
            self.text_field2.insert(1.0,text_field2_value)
        else: 
            text_field1_value = text1Dict_spa.get(dictKey)
            self.text_field1.delete('1.0',END)
            self.text_field1.insert(1.0,text_field1_value)
            text_field2_value = text2Dict_spa.get(dictKey)
            self.text_field2.delete('1.0',END)
            self.text_field2.insert(1.0,text_field2_value)
        
    def copy_text_to_clipboard(self, event): 
        '''Function to copy the clicked text box to the clipboard'''
        text = event.widget.get("1.0","end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
    
            
        
    def run(self):
        self.mainloop()
