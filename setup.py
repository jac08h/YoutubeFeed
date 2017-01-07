import sys
from cx_Freeze import setup, Executable

__author__ = 'KPGM'

# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['atexit', 'cx_Freeze', 'datetime', 'googleapiclient', 'json', 'os', 'urllib', 'xml'],
        'include_files': ['README.md', 'client_secret.json', 'main.ui', 'settings.json', 'subscription_manager.xml']
    }
}

executables = [
    Executable('youtube_feed.py', base=base,
               targetName='YoutubeFeed.exe')
]

setup(name='Youtube Feed',
      version='0.1',
      description='Lists new videos since last checked and add them to your watch later',
      options=options,
      executables=executables
      )
