# This file is part of ReText
# Copyright: Dmitry Shachnev 2012
# License: GNU GPL v2 or higher

import markups
import sys

if '--pyqt4' in sys.argv:
        from PyQt4 import QtCore, QtGui, QtWebKit
elif '--pyside' in sys.argv:
        from PySide import QtCore, QtGui, QtWebKit
else:
	try:
	        from PyQt5 import QtCore, QtPrintSupport, QtGui, QtWidgets, QtWebKit, QtWebKitWidgets
	except ImportError:
	        try:
	                from PyQt4 import QtCore, QtGui, QtWebKit
	        except ImportError:
	                from PySide import QtCore, QtGui, QtWebKit

if not 'QtWidgets' in locals():
        # PyQt4 or PySide
        QtPrintSupport, QtWidgets, QtWebKitWidgets = QtGui, QtGui, QtWebKit

(QByteArray, QDir, QSettings) = (QtCore.QByteArray, QtCore.QDir, QtCore.QSettings)
QFont = QtGui.QFont

app_name = "ReText"
app_version = "4.1.0 (Git)"

settings = QSettings('ReText project', 'ReText')

if not str(settings.fileName()).endswith('.conf'):
	# We are on Windows probably
	settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 
		'ReText project', 'ReText')

try:
	import enchant
	enchant.Dict()
except:
	enchant_available = False
	enchant = None
else:
	enchant_available = True

icon_path = "icons/"

DOCTYPE_NONE = ''
DOCTYPE_MARKDOWN = markups.MarkdownMarkup.name
DOCTYPE_REST = markups.ReStructuredTextMarkup.name
DOCTYPE_HTML = 'html'

configOptions = {
	'appStyleSheet': '',
	'autoPlainText': True,
	'autoSave': False,
	'defaultMarkup': '',
	'editorFont': 'monospace',
	'editorFontSize': 0,
	'font': '',
	'fontSize': 0,
	'iconTheme': '',
	'handleWebLinks': False,
	'hideToolBar': False,
	'highlightCurrentLine': False,
	'lineNumbersEnabled': False,
	'previewState': False,
	'restorePreviewState': False,
	'rightMargin': 0,
	'saveWindowGeometry': False,
	'spellCheck': False,
	'spellCheckLocale': '',
	'styleSheet': '',
	'tabInsertsSpaces': True,
	'tabWidth': 4,
	'useWebKit': False,
	'windowGeometry': QByteArray(),
}

def readFromSettings(key, keytype, settings=settings, default=None):
	if not settings.contains(key):
		return default
	try:
		return settings.value(key, type=keytype)
	except TypeError as error:
		# Type mismatch
		print('Warning: '+str(error))
		# Return an instance of keytype
		return default if (default is not None) else keytype()

def readListFromSettings(key, settings=settings):
	if not settings.contains(key):
		return []
	value = settings.value(key)
	if isinstance(value, str):
		return [value]
	else:
		return value

def writeToSettings(key, value, default, settings=settings):
	if value == default:
		settings.remove(key)
	else:
		settings.setValue(key, value)

def writeListToSettings(key, value, settings=settings):
	if len(value) > 1:
		settings.setValue(key, value)
	elif len(value) == 1:
		settings.setValue(key, value[0])
	else:
		settings.remove(key)

class ReTextSettings(object):
	def __init__(self):
		for option in configOptions:
			value = configOptions[option]
			setattr(self, option, readFromSettings(option,
				type(value), default=value))
	
	def __setattr__(self, option, value):
		if not option in configOptions:
			raise AttributeError('Unknown attribute')
		object.__setattr__(self, option, value)
		writeToSettings(option, value, configOptions[option])

globalSettings = ReTextSettings()

monofont = QFont()
monofont.setFamily(globalSettings.editorFont)
if globalSettings.editorFontSize:
	monofont.setPointSize(globalSettings.editorFontSize)

datadirs = (
	'.',
	'/usr/share/retext',
	'/usr/local/share/retext',
	QDir.homePath()+'/.local/share/retext'
)
