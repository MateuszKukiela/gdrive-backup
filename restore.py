from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import zipfile
import os

UID = int(os.getenv('UID'))
PGID = int(os.getenv('PGID'))


dir_name = '/appdata'

gauth = GoogleAuth()

gauth.LoadCredentialsFile("/credentials/mycreds.txt")
if gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("/credentials/mycreds.txt")

drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': 'title contains ".zip" and trashed=false'}).GetList()
file_list = sorted(file_list, key = lambda i: i['title'])
file_id = file_list[-1]['id']
file_name = file_list[-1]['title']

print(f'Downloading {file_name}')
file = drive.CreateFile({'id': file_id})
zip_path = os.path.join(dir_name, file_name)

file.GetContentFile(zip_path)

print(f'Restoring {file_name}')

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall()

os.remove(zip_path)

for root, dirs, files in os.walk(dir_name):
    for dir_name in dirs:
        os.chown(os.path.join(root, dir_name), UID, PGID)
    for file in files:
        os.chown(os.path.join(root, file), UID, PGID)
print('Done')
