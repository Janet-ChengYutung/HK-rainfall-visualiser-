; NSIS installer script (template)
; Requires makensis to be installed (NSIS) on Windows build agent.

OutFile "HKRainfallInstaller.exe"
InstallDir "$PROGRAMFILES64\HK Rainfall"
RequestExecutionLevel user

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\Main.exe"
  ; Copy data folders if you used onefile you may have to adjust paths
  ; File /r "image\*"
  CreateShortCut "$DESKTOP\HK Rainfall.lnk" "$INSTDIR\Main.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\Main.exe"
  Delete "$DESKTOP\HK Rainfall.lnk"
  RMDir /r "$INSTDIR"
SectionEnd
