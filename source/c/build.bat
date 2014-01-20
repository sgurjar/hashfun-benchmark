@rem call it once to setup env to build
@rem call c:\tools\MicrosoftVisualStudio10.0\VC\bin\vcvars32.bat

@rem ===========================================================================
@rem define USE_WINCRYPTO macro if compiling using Windows CryptoAPI
@rem    http://msdn.microsoft.com/en-us/library/windows/desktop/aa380256
@rem define macro to use USE_WINCRYPTO win32 crypto api   /DUSE_WINCRYPTO
@rem ===========================================================================

@rem c:\tools\MicrosoftVisualStudio10.0\VC\bin\cl.exe

@if not exist build\ mkdir build

@cl.exe ^
  /W4 ^
  /Fobuild\ ^
  /O1 ^
  /DUSE_WINCRYPTO ^
  src\*.c ^
  /link advapi32.lib crypt32.lib /OUT:testhashfuns_win32crypto.exe
