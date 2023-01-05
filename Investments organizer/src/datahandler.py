from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
import os

class DataHandler: 
    def __init__(self): 
        os.chdir(os.path.dirname(__file__))
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

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

    def fetch_data(self): 
        '''
        Function that fetches the data from gdrive
        '''
        SheetId = self.searchObject('Inversiones','root')
        DataSheet = self.drive.CreateFile({'id':SheetId})
        DataSheet.GetContentFile('temp.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        df = pd.read_excel(os.path.join(os.getcwd(),'temp.xlsx'),usecols=None, sheet_name=None,engine='openpyxl')
        df = df['Acciones']
        os.remove('temp.xlsx')
        return df 