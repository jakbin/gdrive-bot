# gdrive-bot

Upload files to your gdrive with gdrive-bot without using google-api-python-client.

 [![Publish package](https://github.com/jakbin/gdrive-bot/actions/workflows/publish.yml/badge.svg)](https://github.com/jakbin/gdrive-bot/actions/workflows/publish.yml)
 [![PyPI version](https://badge.fury.io/py/gdrive-bot.svg)](https://pypi.org/project/gdrive-bot/)
 [![Downloads](https://pepy.tech/badge/gdrive-bot/month)](https://pepy.tech/project/gdrive-bot)
 [![Downloads](https://static.pepy.tech/personalized-badge/gdrive-bot?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/gdrive-bot)
 ![GitHub Contributors](https://img.shields.io/github/contributors/jakbin/gdrive-bot)
 ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jakbin/gdrive-bot)
 ![GitHub last commit](https://img.shields.io/github/last-commit/jakbin/gdrive-bot)
 ![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)


## Features
- Progress bar


## Installation

```sh
pip3 install -U gdrive-bot
```

## Usage 
```sh
g-bot setup               # setup your gdrive credentials
g-bot reset               # reset to default your gdrive credentials
g-bot up {file_name}      # upload gdrive channel or group
g-bot d {url}             # download and upload file to your gdrive
```

# API

The g-bot client is also usable through an API (for test integration, automation, etc)

### g_bot.main.upload_file(access_token:str, filename:str, filedirectory:str, folder_id: str = None)

```py
from g_bot.main import upload_file

upload_file(access_token:str, filename:str, filedirectory:str, folder_id: str = None)
```
