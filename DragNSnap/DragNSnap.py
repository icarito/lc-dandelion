import objc
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

NibClassBuilder.extractClasses("MainMenu")

from DNSView import *
from DNSButton import *

AppHelper.runEventLoop()
