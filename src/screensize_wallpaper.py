import ctypes

SM_CXSCREEN = 0
SM_CYSCREEN = 1
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
SM_CMONITORS = 80

if __name__=='__main__':
	user32 = ctypes.windll.user32
	mainscreensize = user32.GetSystemMetrics(SM_CXSCREEN), user32.GetSystemMetrics(SM_CYSCREEN)
	print mainscreensize
	virtualscreensize = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN), user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
	print virtualscreensize
	screencount = user32.GetSystemMetrics(SM_CMONITORS)
	print screencount
