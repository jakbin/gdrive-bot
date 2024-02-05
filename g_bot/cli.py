import os
import argparse
import configparser
from pathlib import Path
from shutil import copy2

from g_bot import __version__
from g_bot.main import upload_file, download

package_name = "g-bot"

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
access_token = config['GDRIVE']['access_token']
folder_id = config["GDRIVE"]['folder_id']
if folder_id == 'xxxxxxxxxxxxx':
	folder_id = None

def setup():
    print('If you did not want to change anyone, just press enter.')

    access_token = input("Enter your GDRIVE api access token  : ")
    if access_token != '':
        config.set('GDRIVE', 'access_token', access_token)

    folder_id = input("Enter your google drive folder id : ")
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

example_uses = '''example:
   g-bot setup
   g-bot reset
   g-bot up {files_name}
   g-bot d {url}'''

def main(argv = None):
	parser = argparse.ArgumentParser(prog=package_name, description="upload your files to your group or channel", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
	subparsers = parser.add_subparsers(dest="command")

	setup_parser = subparsers.add_parser("setup", help="setup your gdrive credentials")

	reset_parser = subparsers.add_parser("reset", help="reset to default your gdrivr credentials")

	upload_parser = subparsers.add_parser("up", help="upload file to your group or channel")
	upload_parser.add_argument("filename", type=str, help="one or more files to upload")

	download_parser = subparsers.add_parser("d", help="download and upload file to your group or channel")
	download_parser.add_argument("url", type=str, help="url")

	parser.add_argument('-v',"--version",
							action="store_true",
							dest="version",
							help="check version of g-bot")

	args = parser.parse_args(argv)

	if args.command == "setup":
		return setup()
	elif args.command == "reset":
		return reset()
	elif args.command == "up":
		file_name = os.path.basename(args.filename)
		return upload_file(access_token, args.filename, file_name, folder_id)
	elif args.command == "d":
		file_name = os.path.basename(args.url)
		return download(args.url, access_token, folder_id)
	elif args.version:
		return print(__version__)
	else:
		parser.print_help()

if __name__ == '__main__':
	raise SystemExit(main())