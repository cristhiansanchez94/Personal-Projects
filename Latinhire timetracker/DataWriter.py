from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from datetime import date
import os

class DataWriter: 
    def __init__(self): 
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
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
            writer.close()
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
        '''Function that searches for an object over the entire tree of the google drive. It uses a recursive 
        algorithm. 
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
    def searchObjects(self,ObjectsList): 
        '''
        Function that searches through google drive the id's of the objects in 
        ObjectsList
        Inputs: 
         - ObjectsList: List of objects, whose id's are going to be searched
        Outputs: 
         - IdsDict: Dictionary with the id's of the objects in ObjectsList
        '''        
        IdsDict = {Object:None for Object in ObjectsList}
        for Object in IdsDict.keys(): 
            IdsDict[Object] = self.searchObject(Object,'root')
        return IdsDict
    def writeData(self,SheetTitle, FolderTitle,waiting_minutes, working_minutes): 
        '''Function that writes the data to the specified google drive. Whenever 
        file doesn't exist, it creates it depending on the folder title. 
        Inputs: 
         - SheetTitle: The title of the spreadsheet 
         - FolderTitle: The title of the folder. Could be '' 
         - waiting_minutes: The waiting minutes value to be safed
         - working_minutes: The working minutes value to be safed
        '''
        IdsDict = self.searchObjects([SheetTitle, FolderTitle])
        SheetId = IdsDict.get(SheetTitle)
        FolderId = IdsDict.get(FolderTitle)
        if SheetId is None: 
            if FolderTitle == '':
                SheetId = self.createSheet(SheetTitle)
            else: 
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
        df[sheet_name] = df[sheet_name].append({'Date':current_date,'Working minutes':working_minutes,'Waiting minutes':waiting_minutes},ignore_index=True)
        with pd.ExcelWriter('output.xlsx') as writer: 
            for month in months: 
                df[month].to_excel(writer,sheet_name=month,index=False)
            writer.save()
            writer.close()
        DataSheet.SetContentFile('output.xlsx')
        DataSheet.Upload()
    