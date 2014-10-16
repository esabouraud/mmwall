python detdownload_wallpaper.py -s
python synergy_wallpaper.py -L
python ftpsync_wallpaper.py -H localhost -s -i 1
rem set WALLUSER=DOMAIN\USER
rem set WALLPASS=PASSWORD
psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -i -w "D:\Users\esabouraud\src\my-projects\scripts\wallpaper" "D:\Users\esabouraud\src\my-projects\scripts\wallpaper\wallcli.bat"
rem python setup.py py2exe
rem copy ftpsync_wallpaper.py C:\Temp
rem psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -i -c -f -w C:\Temp C:\Temp\ftpsync_wallpaper.py -H 192.168.1.96 -i 0
pause
