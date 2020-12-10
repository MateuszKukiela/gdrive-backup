from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import sys
import zipfile
from datetime import date

dir_name = '/appdata'

f = open("/REMAIN.txt", "r")
REMAIN = int(f.read()) - 1

f = open("/TEAM_ID.txt", "r")
TEAM_ID = str(f.read()).rstrip()

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
    file_list = drive.ListFile({'q': 'title contains ".zip" and trashed=false and "root" in parents'}).GetList()
    file_list = sorted(file_list, key=lambda i: i['title'], reverse=True)
    for file in file_list[REMAIN:]:
        file['parents'] = [{"kind": "drive#fileLink", "id": TEAM_ID}]
        file.Upload()

    backup_file = drive.CreateFile({'title': today + '.zip'})
    backup_file.SetContentFile(zip_path)
    backup_file.Upload()

    print('Done')
except:
    e = sys.exc_info()[0]
    print(e)
    print('Failed')

os.remove(zip_path)


