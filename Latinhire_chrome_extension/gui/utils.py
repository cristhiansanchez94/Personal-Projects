from datetime import datetime 
def calculate_minutes(counter): 
    '''Function that calculates the total amount of time, in minutes, from the counter
    Inputs: 
     -counter: counter to be used to calculate the minutes of the timestamp
    Outputs: 
     -time_in_minutes: the total amount of minutes of the timestamp represented by counter
    '''
    dt = datetime.fromtimestamp(counter)
    time_in_minutes = dt.hour*60 + dt.minute + (dt.second)/60
    return time_in_minutes

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