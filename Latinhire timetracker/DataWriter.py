from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os 
print(os.getcwd())
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in fileList: 
    print('Title: %s, ID: %s' % (file['title'], file['id']))