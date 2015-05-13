# http://stackoverflow.com/questions/18662430/what-would-cause-this-code-to-produce-different-results-when-running-at-the-modu
import ctypes
from ctypes import wintypes 
from collections import namedtuple

LPRECT = ctypes.POINTER(wintypes.RECT)

# Callback Factory
MonitorEnumProc = ctypes.WINFUNCTYPE(
	ctypes.c_bool, 
	wintypes.HMONITOR,
	wintypes.HDC,
	LPRECT,
	wintypes.LPARAM)

ctypes.windll.user32.EnumDisplayMonitors.restype = wintypes.BOOL
ctypes.windll.user32.EnumDisplayMonitors.argtypes = [
	wintypes.HDC,
	LPRECT,
	MonitorEnumProc,
	wintypes.LPARAM]

SCREENS = []
ScreenRC = namedtuple("ScreenRC", "left top right bottom")

def _monitorEnumProc(hMonitor, hdcMonitor, lprcMonitor, dwData):
	#print 'call result:', hMonitor, hdcMonitor, lprcMonitor, dwData
	screen = ScreenRC(lprcMonitor[0].left, lprcMonitor[0].top, lprcMonitor[0].right, lprcMonitor[0].bottom)
	SCREENS.append(screen)
	return True # continue enumeration

# Make the callback function
enum_callback = MonitorEnumProc(_monitorEnumProc)

def enum_mons():   
	'''Enumerate the display monitors.'''
	return ctypes.windll.user32.EnumDisplayMonitors(
		None, 
		None,
		enum_callback,
		0)

def screens_size():
	sizes = [(s.right - s.left, s.bottom - s.top, s.top) for s in SCREENS]
	print sizes

if __name__ == '__main__':
	print 'return code: %d' % enum_mons()
	print SCREENS
	screens_size()