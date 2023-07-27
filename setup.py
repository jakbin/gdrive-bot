import setuptools
from g_bot import __version__

with open("README.md", "r") as readme_file:
	readme = readme_file.read()

setuptools.setup(
	name="gdrive-bot",
	version=__version__,
	author="Jak Bin",
	author_email="jakbin4747@gmail.com",
	description="upload files to gdrive with access token",
	long_description=readme,
	long_description_content_type="text/markdown",
	url="https://github.com/jakbin/g-bot",
	install_requires=["tqdm","requests","requests-toolbelt"],
	python_requires=">=3",
	project_urls={
		"Bug Tracker": "https://github.com/jakbin/g-bot/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
	],
	keywords='gdrive,g-bot,gdrive-api,gdrive-api-bot,gdrive-file-upload,gdrive-upload',
	packages=["g_bot"],
	package_data={  
		'g_bot': [
			'config.ini',
		]},
	entry_points={
		"console_scripts":[
			"g-bot = g_bot.cli:main"
		]
	}
)