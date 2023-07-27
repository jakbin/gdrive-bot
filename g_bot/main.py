import os
import sys
import json
import urllib3
import requests
import collections
import configparser
from tqdm import tqdm
from pathlib import Path
from shutil import copy2
import requests_toolbelt
import urllib.parse as urlparse
from requests.exceptions import JSONDecodeError
from requests.exceptions import MissingSchema
from requests import get, ConnectionError, head

urllib3.disable_warnings()

base_dir = os.path.dirname(os.path.realpath(__file__))
config = os.path.join(base_dir, 'config.ini')

home_path = Path.home()
if os.path.isfile(os.path.join(home_path, ".config/g-bot/config.ini")):
    config_file = os.path.join(home_path, ".config/g-bot/config.ini")
else:
    if not os.path.isdir(os.path.join(home_path, '.config/g-bot')):
        os.mkdir(os.path.join(home_path, '.config/g-bot'))
    copy2(config,os.path.join(home_path, ".config/g-bot"))
    config_file = os.path.join(home_path, ".config/g-bot/config.ini")

config = configparser.ConfigParser()
config.read(config_file)

class ProgressBar(tqdm):
    def update_to(self, n: int) -> None:
        self.update(n - self.n)

def setup():
    print('If you did not want to change anyone, just press enter.')

    access_token = input("Enter your GDRIVE api access token  : ")
    if access_token != '':
        config.set('GDRIVE', 'access_token', access_token)

    folder_id = input("Enter your channel name or chat id with '-' : ")
    if folder_id != '':
        config.set('GDRIVE', 'folder_id', folder_id)

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print("Setup complete!")

def reset():
    config.set('GDRIVE', 'folder_id', 'xxxxxxxxxxxxx')
    config.set('GDRIVE', 'access_token', '1234567890xxxxxxx')

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print("Config file has been reset to default!") 

def upload_file(access_token:str, filename:str, filedirectory:str, folder_id: str = None):

    if folder_id == None:
        metadata = {
            "name": filename,
            "parents": [folder_id]
        }
    else:
        metadata = {
            "name": filename,
            "parents": [folder_id]
        }

    session = requests.session()

    with open(filedirectory, "rb") as fp:
        files = collections.OrderedDict(data=("metadata", json.dumps(metadata), "application/json"), file=fp)
        encoder = requests_toolbelt.MultipartEncoder(files)
        with ProgressBar(
            total=encoder.len,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            file=sys.stdout,
        ) as bar:
            monitor = requests_toolbelt.MultipartEncoderMonitor(
                encoder, lambda monitor: bar.update_to(monitor.bytes_read)
            )

            r = session.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true",
                data=monitor,
                allow_redirects=False,
                json=metadata,
                headers={"Authorization": "Bearer " + access_token, "Content-Type": monitor.content_type},
            )

    try:
        resp = r.json()
        print(resp)
    except JSONDecodeError:
        sys.exit(r.text)


def downloader(url:str, file_name:str):
    try:
        filesize = int(head(url).headers["Content-Length"])
    except ConnectionError:
        sys.exit("[Error]: No internet")
    except MissingSchema as e:
        sys.exit(str(e))
    except KeyError:
        filesize = None

    chunk_size = 1024

    try:
        with get(url, stream=True) as r, open(file_name, "wb") as f, tqdm(
                unit="B",  # unit string to be displayed.
                unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
                unit_divisor=1024,  # is used when unit_scale is true
                total=filesize,  # the total iteration.
                file=sys.stdout,  # default goes to stderr, this is the display on console.
                desc=file_name  # prefix to be displayed on progress bar.
        ) as progress:
            for chunk in r.iter_content(chunk_size=chunk_size):
                datasize = f.write(chunk)
                progress.update(datasize)
    except ConnectionError as e:
        print(e)

def filename_from_url(url):
    fname = os.path.basename(urlparse.urlparse(url).path)
    if len(fname.strip(" \n\t.")) == 0:
        return None
    return fname

def filename_from_headers(headers):
    if type(headers) == str:
        headers = headers.splitlines()
    if type(headers) == list:
        headers = dict([x.split(':', 1) for x in headers])
    cdisp = headers.get("Content-Disposition")
    if not cdisp:
        return None
    cdtype = cdisp.split(';')
    if len(cdtype) == 1:
        return None
    if cdtype[0].strip().lower() not in ('inline', 'attachment'):
        return None
    # several filename params is illegal, but just in case
    fnames = [x for x in cdtype[1:] if x.strip().startswith('filename=')]
    if len(fnames) > 1:
        return None
    name = fnames[0].split('=')[1].strip(' \t"')
    name = os.path.basename(name)
    if not name:
        return None
    return name

def detect_filename(url=None, headers=None):
    names = dict(out='', url='', headers='')
    if url:
        names["url"] = filename_from_url(url) or ''
    if headers:
        names["headers"] = filename_from_headers(headers) or ''
    return names["out"] or names["headers"] or names["url"]

def download(url:str, access_token:str, folder_id:str = None):
    download_path = 'downloads'
    if not os.path.isdir(download_path):
        os.mkdir(download_path)

    filename = detect_filename(url, head(url).headers)

    yes = {'yes','y','ye',''}
    choice = input(f"Do you want change filename {filename[0:60]} [Y/n]: ").lower()
    if choice in yes:
        filename = input("Enter new file name with extension: ")

    file_path = os.path.join(download_path, filename)

    print("Downloading file......")
    try:
        downloader(url, file_path)
    except OSError:
        print("File name is too log !")
        filename = input("Enter new filename : ")
        file_path = os.path.join(download_path, filename)
        downloader(url, file_path)
    
    print("\nUploading file......")
    filedirectory = f"downloads/{filename}"
    upload_file(access_token, filename, filedirectory, folder_id)
