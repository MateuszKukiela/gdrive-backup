from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import zipfile
from datetime import date

dir_name = '/appdata'

gauth = GoogleAuth()

gauth.LoadCredentialsFile("/credentials/mycreds.txt")
if gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("/credentials/mycreds.txt")

drive = GoogleDrive(gauth)


def retrieve_file_paths(dirName):
    file_paths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths


file_paths = retrieve_file_paths(dir_name)

today = date.today().strftime("%Y-%m-%d")

zip_path = os.path.join(dir_name, today + '.zip')

zip_file = zipfile.ZipFile(zip_path, 'w')

print(f'Backing up to {today}.zip')

with zip_file:
    for file in file_paths:
        zip_file.write(file)

try:
    file1 = drive.CreateFile({'title': today + '.zip'})
    file1.SetContentFile(zip_path)
    file1.Upload()
    file_list = drive.ListFile({'q': 'title contains ".zip" and trashed=false'}).GetList()
    file_list = sorted(file_list, key=lambda i: i['title'])
    for file in file_list[5:]:
        file.Trash()
    print('Done')
except:
    print('Failed')

os.remove(zip_path)


