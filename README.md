# mmwall

mmwall is a tool written in Python 2 (>= 2.6) that sets a single wallpaper on a multi-screen, multi-machine setup.
I wrote it to have a single background image spanning multiple screens and machines, especially when using a software KM switch (like Synergy).

The way it works is:
  1. download an image from a random supported source
  2. resize it and cut it to match screen configuration
  3. push script and wallpaper on each machine then run script remotely to apply wallpaper (Windows and RHEL/CentOS only for now)

Its mandatory dependencies are:
  * BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)
  * Python Imaging Library (http://www.pythonware.com/products/pil/) or Pillow (https://github.com/python-pillow/Pillow)
  
Its Windows specific dependencies are:
  * PsExec (https://technet.microsoft.com/en-us/sysinternals/bb897553)
  * PuTTY, PSFTP (http://www.chiark.greenend.org.uk/~sgtatham/putty/)


