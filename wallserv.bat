@rem Do the heavy lifting
@rem WALLFTP must be set (localhost, 192.168.1.1...)
python detdownload_wallpaper.py -s
python synergy_wallpaper.py -L
python ftpsync_wallpaper.py -H %WALLFTP% -s -i 1
python set_wallpaper.py -i 1

@rem Poor man's RPC to set wallpaper on client
@rem WALLHOST, WALLUSER and WALLPASS must be set
@rem using FTP to download wallpapers kinda pointless now...
net use t: \\%WALLHOST%\C$\Temp /user:%WALLUSER% %WALLPASS%
copy ftpsync_wallpaper.py t:
copy set_wallpaper.py t:
echo python ftpsync_wallpaper.py -H %WALLFTP% -i 0 > t:\wallcli.bat
echo python set_wallpaper.py -i 0 >> t:\wallcli.bat
psexec \\%WALLHOST% -u %WALLUSER% -p %WALLPASS% -i -w "C:\Temp" "C:\Temp\wallcli.bat"
del t:\ftpsync_wallpaper.py
del t:\set_wallpaper.py t:
del t:\wallcli.bat
net use t: /d
