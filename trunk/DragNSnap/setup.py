'''
Minimal setup.py example, run with:
% python setup.py py2app
'''

from setuptools import setup

NAME = "DragNSnap"
SCRIPT = "DragNSnap.py"
VERSION = "0.1.0"
ICON = "DragnSnap.icns"
ID = "drag_n_snap"
COPYRIGHT = "Copyright 2007 Dethe Elza"
DATA_FILES = ['English.lproj']

plist = dict(
    CFBundleIconFile            = ICON,
    CFBundleName     = NAME,
    CFBundleShortVersionString = ' '.join([NAME, VERSION]),
    CFBundleGetInfoString = NAME,
    CFBundleExecutable = NAME,
    CFBundleIdentifier = 'org.livingcode.applications.%s' % ID,
    NSHumanReadableCopyright = COPYRIGHT,
)

py2app_opt = dict(plist=plist)

setup(app=[SCRIPT],
    setup_requires=['py2app'],
    data_files=DATA_FILES,
    options=dict(
        py2app=dict(
            plist=plist,
        ),
    ),
)


