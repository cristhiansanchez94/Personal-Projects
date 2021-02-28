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
    def searchObjects(self,ObjectsList): 
        '''
        Function that searches through google drive the id's of the objects in 
        ObjectsList
        Inputs: 
         - ObjectsList: List of objects, whose id's are going to be searched
        Outputs: 
         - IdsDict: Dictionary with the id's of the objects in ObjectsList
        '''
        fileList = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        IdsDict = {Object:None for Object in ObjectsList}
        for file in fileList: 
            if file['title'] in IdsDict.keys(): 
                IdsDict[file['title']] = file['id']
        return IdsDict