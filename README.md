# mmwall

mmwall is a tool written in Python 2 (>= 2.6) that sets a single wallpaper on a multi-screen, multi-machine setup.
I wrote it to have a single background image spanning multiple screens and machines, especially when using a software KM switch (like Synergy).

The way it works is by running the following on a "master" machine:
  1. download an image from a supported source of background wallpapers
  2. resize and cut it to fit the entire multiple screen surface
  3. upload wallpaper data to remote machines (SMB on Windows, SFTP on Linux)
  3. trigger execution on remote hosts of script to apply wallpaper (PsExec on Windows, SSH on Linux)

Supported platforms are : Windows >= XP, Linux distributions using Gnome 2.

Its common dependencies are:
  * (all) Python >= 2.6 (https://www.python.org/)
  * (all) Python Imaging Library (http://www.pythonware.com/products/pil/) or Pillow (https://github.com/python-pillow/Pillow)
  * (master) BeautifulSoup4 (http://www.crummy.com/software/BeautifulSoup/)
  * (master) lxml (http://lxml.de/)
  
Its Windows specific dependencies are:
  * (master) PsExec (https://technet.microsoft.com/en-us/sysinternals/bb897553)
  * (master) PuTTY, PSFTP (http://www.chiark.greenend.org.uk/~sgtatham/putty/)

Its Linux specific dependencies are:
  * (master) libjpeg-devel libpng-devel
  * (master) ssh sftp sshpass 
  * (remote) sshd
