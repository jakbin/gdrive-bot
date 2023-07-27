import os
import argparse
import configparser

from g_bot import __version__
from g_bot.main import setup, reset, upload_file, download, config_file

package_name = "g-bot"

config = configparser.ConfigParser()
config.read(config_file)
access_token = config['GDRIVE']['access_token']
folder_id = config["GDRIVE"]['folder_id']
if folder_id == 'xxxxxxxxxxxxx':
	folder_id = None

example_uses = '''example:
   g-bot setup
   g-bot reset
   g-bot up {files_name}
   g-bot d {url}'''

def main(argv = None):
	parser = argparse.ArgumentParser(prog=package_name, description="upload your files to your group or channel", epilog=example_uses, formatter_class=argparse.RawDescriptionHelpFormatter)
	subparsers = parser.add_subparsers(dest="command")

	setup_parser = subparsers.add_parser("setup", help="setup your gdrivr credentials")

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