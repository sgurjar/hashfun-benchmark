@rem call it once to setup env to build
@rem call c:\tools\MicrosoftVisualStudio10.0\VC\bin\vcvars32.bat

@rem ===========================================================================
@rem define USE_WINCRYPTO macro if compiling using Windows CryptoAPI
@rem    http://msdn.microsoft.com/en-us/library/windows/desktop/aa380256
@rem define macro to use USE_WINCRYPTO win32 crypto api   /DUSE_WINCRYPTO
@rem ===========================================================================

@rem c:\tools\MicrosoftVisualStudio10.0\VC\bin\cl.exe

@if not exist build\ mkdir build

@rem cl.exe ^
@rem   /W4 ^
@rem   /Fobuild\ ^
@rem   /O1 ^
@rem   /DUSE_WINCRYPTO ^
@rem   src\common.c src\testhashfuns.c src\testwin32crypto.c ^
@rem   /link advapi32.lib crypt32.lib /OUT:testhashfuns_win32crypto.exe

@rem rmdir build\*

@rem include openssl headers
@rem set INCLUDE=%INCLUDE%;c:\tools\openssl\openssl-1.0.0l\inc32;

@cl.exe ^
 /W4 ^
 /Fobuild\ ^
 /O1 ^
 /DUSE_OPENSSL ^
 src\common.c src\testhashfuns.c src\testopenssl.c ^
 /link advapi32.lib user32.lib gdi32.lib c:\tools\openssl\openssl-1.0.0l\out32\libeay32.lib ^
 /OUT:testhashfuns_openssl.exe
