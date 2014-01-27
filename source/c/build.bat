@rem call it once to setup env to build
@rem call c:\tools\MicrosoftVisualStudio10.0\VC\vcvarsall.bat

@if not exist build_wincrypto\ (
  mkdir build_wincrypto
) else (
  del /q build_wincrypto\*
)
@if not exist build_openssl\ (
  mkdir build_openssl
) else (
  del /q build_openssl\*
)

cl.exe ^
/nologo ^
/MT ^
/Ox ^
/O2 ^
/Ob2 ^
/W3 ^
/WX ^
/Gs0 ^
/GF ^
/Gy ^
/Fobuild_wincrypto\ ^
/DUSE_WINCRYPTO ^
/DWIN32_LEAN_AND_MEAN ^
/D_CRT_SECURE_NO_DEPRECATE ^
-c ^
src\common.c src\testhashfuns.c src\testwin32crypto.c

@if %ERRORLEVEL% GTR 0 goto :eof

link.exe ^
/nologo ^
/opt:ref ^
advapi32.lib crypt32.lib ^
/OUT:testhashfuns_win32crypto.exe ^
build_wincrypto\common.obj build_wincrypto\testhashfuns.obj build_wincrypto\testwin32crypto.obj

@if %ERRORLEVEL% GTR 0 goto :eof

cl.exe ^
/nologo ^
/Ic:\tools\openssl\openssl-1.0.0l\inc32 ^
/MT ^
/Ox ^
/O2 ^
/Ob2 ^
/W3 ^
/WX ^
/Gs0 ^
/GF ^
/Gy ^
/Fobuild_openssl\ ^
/DUSE_OPENSSL ^
/DWIN32_LEAN_AND_MEAN ^
/D_CRT_SECURE_NO_DEPRECATE ^
-c ^
src\common.c src\testhashfuns.c src\testopenssl.c

@if %ERRORLEVEL% GTR 0 goto :eof

link.exe ^
/nologo ^
/opt:ref ^
advapi32.lib user32.lib gdi32.lib c:\tools\openssl\openssl-1.0.0l\out32\libeay32.lib ^
/OUT:testhashfuns_openssl.exe ^
build_openssl\common.obj build_openssl\testhashfuns.obj build_openssl\testopenssl.obj
