@rem Do the heavy lifting
@rem WALLFTP must be set (localhost, 192.168.1.1...)
python detdownload_wallpaper.py -s
python synergy_wallpaper.py -L
python ftpsync_wallpaper.py -H %WALLFTP% -s -i 1

@rem Poor man's RPC to set wallpaper on client
net use t: \\frws2250\C$\Temp /user:%WALLUSER% %WALLPASS%
copy ftpsync_wallpaper.py t:
echo python ftpsync_wallpaper.py -H %WALLFTP% -i 0 > t:\wallcli.bat
psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -i -w "C:\Temp" "C:\Temp\wallcli.bat"
del t:\ftpsync_wallpaper.py
del t:\wallcli.bat
net use t: /d

@rem set WALLUSER=DOMAIN\USER
@rem set WALLPASS=PASSWORD
@rem psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -i -w "D:\Users\esabouraud\src\my-projects\scripts\wallpaper" "D:\Users\esabouraud\src\my-projects\scripts\wallpaper\wallcli.bat"

@rem copy wallcliwrap.bat C:\Temp
@rem type ftpsync_wallpaper.py >> C:\Temp\wallcliwrap.bat
@rem copy ftpsync_wallpaper.py C:\Temp
@rem psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -h -i -c -f -w C:\Temp C:\Temp\ftpsync_wallpaper.py -H 192.168.1.96 -i 0

@rem python setup.py py2exe
@rem copy ftpsync_wallpaper.py C:\Temp
@rem psexec \\frws2250 -u %WALLUSER% -p %WALLPASS% -i -c -f -w C:\Temp C:\Temp\ftpsync_wallpaper.py -H 192.168.1.96 -i 0
@rem pause
