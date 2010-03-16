; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Friture"
!define PRODUCT_VERSION "20100316"
!define PRODUCT_PUBLISHER "Timoth�e Lecomte"
!define PRODUCT_WEB_SITE "http://wiki.github.com/tlecomte/friture/"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\friture.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "COPYING"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\friture.exe"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "French"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "friture-setup-${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES\Friture"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
FunctionEnd

Section "SectionPrincipale" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite try
  File "dist\API-MS-Win-Core-LocalRegistry-L1-1-0.dll"
  File "dist\API-MS-Win-Core-ProcessThreads-L1-1-0.dll"
  File "dist\API-MS-Win-Security-Base-L1-1-0.dll"
  File "dist\bz2.pyd"
  File "dist\friture.exe"
  CreateDirectory "$SMPROGRAMS\Friture"
  CreateShortCut "$SMPROGRAMS\Friture\Friture.lnk" "$INSTDIR\friture.exe"
  CreateShortCut "$DESKTOP\Friture.lnk" "$INSTDIR\friture.exe"
  SetOutPath "$INSTDIR\imageformats"
  File "dist\imageformats\qsvg4.dll"
  SetOutPath "$INSTDIR"
  File "dist\KERNELBASE.dll"
  File "dist\library.zip"
  File "dist\numpy.core.multiarray.pyd"
  File "dist\numpy.core.scalarmath.pyd"
  File "dist\numpy.core.umath.pyd"
  File "dist\numpy.core._dotblas.pyd"
  File "dist\numpy.core._sort.pyd"
  File "dist\numpy.fft.fftpack_lite.pyd"
  File "dist\numpy.lib._compiled_base.pyd"
  File "dist\numpy.linalg.lapack_lite.pyd"
  File "dist\numpy.random.mtrand.pyd"
  File "dist\POWRPROF.dll"
  File "dist\pyexpat.pyd"
  File "dist\PyQt4.Qt.pyd"
  File "dist\PyQt4.QtCore.pyd"
  File "dist\PyQt4.QtGui.pyd"
  File "dist\PyQt4.QtSvg.pyd"
  File "dist\PyQt4.Qwt5.Qwt.pyd"
  File "dist\python26.dll"
  File "dist\pywintypes26.dll"
  File "dist\QtCore4.dll"
  File "dist\QtGui4.dll"
  File "dist\QtSvg4.dll"
  File "dist\select.pyd"
  File "dist\sgmlop.pyd"
  File "dist\sip.pyd"
  File "dist\unicodedata.pyd"
  File "dist\w9xpopen.exe"
  File "dist\win32api.pyd"
  File "dist\win32evtlog.pyd"
  File "dist\win32pdh.pyd"
  File "dist\_ctypes.pyd"
  File "dist\_hashlib.pyd"
  File "dist\_multiprocessing.pyd"
  File "dist\_portaudio.pyd"
  File "dist\_socket.pyd"
SectionEnd

Section -AdditionalIcons
  CreateShortCut "$SMPROGRAMS\Friture\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\friture.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\friture.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) a �t� d�sinstall� avec succ�s de votre ordinateur."
FunctionEnd

Function un.onInit
!insertmacro MUI_UNGETLANGUAGE
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "�tes-vous certains de vouloir d�sinstaller totalement $(^Name) et tous ses composants ?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\_socket.pyd"
  Delete "$INSTDIR\_portaudio.pyd"
  Delete "$INSTDIR\_multiprocessing.pyd"
  Delete "$INSTDIR\_hashlib.pyd"
  Delete "$INSTDIR\_ctypes.pyd"
  Delete "$INSTDIR\win32pdh.pyd"
  Delete "$INSTDIR\win32evtlog.pyd"
  Delete "$INSTDIR\win32api.pyd"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\unicodedata.pyd"
  Delete "$INSTDIR\sip.pyd"
  Delete "$INSTDIR\sgmlop.pyd"
  Delete "$INSTDIR\select.pyd"
  Delete "$INSTDIR\QtSvg4.dll"
  Delete "$INSTDIR\QtGui4.dll"
  Delete "$INSTDIR\QtCore4.dll"
  Delete "$INSTDIR\pywintypes26.dll"
  Delete "$INSTDIR\python26.dll"
  Delete "$INSTDIR\PyQt4.Qwt5.Qwt.pyd"
  Delete "$INSTDIR\PyQt4.QtSvg.pyd"
  Delete "$INSTDIR\PyQt4.QtGui.pyd"
  Delete "$INSTDIR\PyQt4.QtCore.pyd"
  Delete "$INSTDIR\PyQt4.Qt.pyd"
  Delete "$INSTDIR\pyexpat.pyd"
  Delete "$INSTDIR\POWRPROF.dll"
  Delete "$INSTDIR\numpy.random.mtrand.pyd"
  Delete "$INSTDIR\numpy.linalg.lapack_lite.pyd"
  Delete "$INSTDIR\numpy.lib._compiled_base.pyd"
  Delete "$INSTDIR\numpy.fft.fftpack_lite.pyd"
  Delete "$INSTDIR\numpy.core._sort.pyd"
  Delete "$INSTDIR\numpy.core._dotblas.pyd"
  Delete "$INSTDIR\numpy.core.umath.pyd"
  Delete "$INSTDIR\numpy.core.scalarmath.pyd"
  Delete "$INSTDIR\numpy.core.multiarray.pyd"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\KERNELBASE.dll"
  Delete "$INSTDIR\imageformats\qsvg4.dll"
  Delete "$INSTDIR\friture.exe"
  Delete "$INSTDIR\bz2.pyd"
  Delete "$INSTDIR\API-MS-Win-Security-Base-L1-1-0.dll"
  Delete "$INSTDIR\API-MS-Win-Core-ProcessThreads-L1-1-0.dll"
  Delete "$INSTDIR\API-MS-Win-Core-LocalRegistry-L1-1-0.dll"

  Delete "$SMPROGRAMS\Friture\Uninstall.lnk"
  Delete "$DESKTOP\Friture.lnk"
  Delete "$SMPROGRAMS\Friture\Friture.lnk"

  RMDir "$SMPROGRAMS\Friture"
  RMDir "$INSTDIR\imageformats"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd