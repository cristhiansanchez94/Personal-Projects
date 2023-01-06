from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from datetime import date
import os

class DataWriter: 
    def __init__(self):
        os.chdir(os.path.dirname(__file__))
        self.gauth = GoogleAuth()
        self.gauth.LoadClientConfig()
        self.check_auth_conn()
        self.drive = GoogleDrive(self.gauth)
        
    def check_auth_conn(self): 
        if self.gauth.credentials is None: 
            self.gauth.LocalWebserverAuth()  
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()

    def createSheet(self,SheetTitle,FolderId=None):
        '''Function that creates a google sheets at the specified folder. If no folder 
        is specified, the sheet is created at the root
        Inputs: 
        -SheetTitle: The title of the sheet to be created 
        -FolderId: The ID of the folder where the sheet will be created 
        Outputs: 
        -SheetId: The ID of the created sheet'''
        if FolderId ==None: 
            file = self.drive.CreateFile({'title':SheetTitle+'.xlsx'})
        else:            
            file = self.drive.CreateFile({'title':SheetTitle+'.xlsx',
            'parents': [{'kind': 'drive#fileLink','id': FolderId}]})
        months =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        with pd.ExcelWriter('output.xlsx') as writer: 
            df = pd.DataFrame(columns=['Date','Working minutes','Waiting minutes'])
            for month in months: 
                df.to_excel(writer,sheet_name=month,index=False)
            writer.save()
        file.SetContentFile('output.xlsx')
        file['title']=SheetTitle
        file.Upload()
        SheetId=file['id']
        return SheetId

    def createFolder(self,FolderTitle):
        '''Function that creates a folder with title FolderTitle. The folder is created at the root.
        Inputs: 
        -FolderTitle: The title of the folder to be created 
        Outputs: 
        -FolderId: The ID of the created folder'''
        folder = self.drive.CreateFile({'title':FolderTitle,'mimeType':'application/vnd.google-apps.folder'})
        folder.Upload()
        FolderId = folder['id']
        return FolderId

    def searchObject(self,searchedObjectTitle, parent_folder_id):
        '''Function that searches for an object over the entire tree of the google drive. 
        It uses a recursive algorithm. 
        Inputs: 
         -searchedObjectTitle: The title of the searched object 
         - parent_folder_id: The id of the current folder where the algorithm is searching for the file
        Outpus: 
         - founId: The id of the searched File. It is None if it's not found.
        '''
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % parent_folder_id}).GetList()
        foundId = None
        for file in file_list: 
            if file['title'] == searchedObjectTitle: 
                return file['id']
            if file['mimeType']=='application/vnd.google-apps.folder': 
                foundId = self.searchObject(searchedObjectTitle,file['id'])
        return foundId 

    def writeData(self,SheetTitle, FolderTitle,waiting_minutes, working_minutes,number_of_sessions): 
        '''Function that writes the data to the specified google drive. Whenever 
        file doesn't exist, it creates it depending on the folder title. 
        Inputs: 
         - SheetTitle: The title of the spreadsheet 
         - FolderTitle: The title of the folder. Could be '' 
         - waiting_minutes: The waiting minutes value to be safed
         - working_minutes: The working minutes value to be safed
        '''
        SheetId = self.searchObject(SheetTitle,'root')
        if SheetId is None: 
            SheetId = self.searchObject(SheetTitle+'.xlsx','root')
            if SheetId is None:
                if FolderTitle == '':
                    SheetId = self.createSheet(SheetTitle)
                else: 
                    FolderId = self.searchObject(FolderTitle,'root')
                    if FolderId is None:
                        FolderId = self.createFolder(FolderTitle)
                    SheetId = self.createSheet(SheetTitle, FolderId = FolderId)
        DataSheet = self.drive.CreateFile({'id':SheetId})
        DataSheet.GetContentFile('temp.xlsx')
        months =['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        current_date = date.today()
        current_month = current_date.month
        sheet_name = months[current_month-1]
        df = pd.read_excel(os.path.join(os.getcwd(),'temp.xlsx'),usecols=None, sheet_name=None,engine='openpyxl')
        df[sheet_name] = df[sheet_name].append({'Date':current_date,'Working minutes':working_minutes,'Waiting minutes':waiting_minutes, 'Number of sessions': number_of_sessions},ignore_index=True)
        df[sheet_name]['Working earnings'] = df[sheet_name]['Working minutes']*6/60
        df[sheet_name]['Waiting earnings'] = df[sheet_name]['Waiting minutes']*3/60
        df[sheet_name]['Total earnings'] = df[sheet_name]['Waiting earnings']+ df[sheet_name]['Working earnings']
        with pd.ExcelWriter('output.xlsx') as writer: 
            for month in months: 
                df[month].to_excel(writer,sheet_name=month,index=False)
            writer.save()
        DataSheet.SetContentFile('output.xlsx')
        DataSheet.Upload()
        os.remove('output.xlsx')
        os.remove('temp.xlsx')
