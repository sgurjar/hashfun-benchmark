import os, os.path, subprocess, platform

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(BASEDIR,'data')
SRCDIR  = os.path.join(BASEDIR,'source')

JAVA_CMD    = 'c:/tools/jdk/jdk1.7.0_25/bin/java.exe'
PYTHON_CMD  = 'c:/tools/python/Python275/python.exe'
PERL_CMD    = 'c:/tools/perl/strawberry/perl/bin/perl.exe'

REPEAT_COUNT    = '1'
WARMPUP_COUNT   = '1'

HASH_ALGORITHMS = ('md5','sha1','sha256','sha512')

DATAFILES       = filter(lambda x: x.endswith('.dat'), os.listdir(DATADIR))

#----------------------
def platform_info():
    info={}
    if platform.system().lower().startswith('win'): # windows use wmic

        cpuinfo=dict(x.split('=',1) for x in subprocess.check_output(
            'wmic cpu get name,caption,numberofcores /format:value'.split()).
            splitlines() if x)

        info['processor']=cpuinfo['Caption']
        info['cpu'      ]=cpuinfo['Name']
        info['cores'    ]=cpuinfo['NumberOfCores']

        osinfo = dict(x.split('=',1) for x in subprocess.check_output(
        'wmic os get caption,osarchitecture,totalvisiblememorysize /format:value'.
            split()).splitlines() if x)

        info['os']=osinfo['Caption'] + osinfo['OSArchitecture']
        info['ram']=osinfo['TotalVisibleMemorySize']

    print '##',info['os']
    print '##',info['processor']
    print '##',info['cpu']+', #cores',info['cores']
    print '##','RAM',info['ram'],'bytes'

#----------------------
def runtest(**kwargs):
    for datafile in DATAFILES:
        for algo in HASH_ALGORITHMS:
            try:
                for line in subprocess.check_output(
                        kwargs['getargs'](algo, datafile)).splitlines():
                    print kwargs['prefix'], algo, datafile, line
            except subprocess.CalledProcessError as e:
                print e.retcode, e.cmd, e.output

#----------------------
def runjava(java_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ java_cmd,
                 '-server', '-Xms512M', '-Xmx512M', # server vm with 512 mb
                 '-cp', SRCDIR + '/java/build',
                 'testhashfuns',
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='java', getargs=getargs)

#----------------------
def runpython(python_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ python_cmd,
                 SRCDIR + '/python/testhashfuns.py',
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='python', getargs=getargs)

#----------------------
def runcsharp(cs_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ cs_cmd,
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='c#', getargs=getargs)

#----------------------
def runwincrypto(cwin_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ cwin_cmd,
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='c_wincrypto', getargs=getargs)

#----------------------
def runperl(perl_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ perl_cmd,
                 'source/perl/testhashfuns.pl',
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='perl', getargs=getargs)

#----------------------
def main():
    platform_info()
    cs_exe = 'source/c#/testhashfuns_cs.exe'
    c_wincrypto_exe = 'source/c/testhashfuns_win32crypto.exe'

    #runjava     (JAVA_CMD       , REPEAT_COUNT, WARMPUP_COUNT)
    #runpython   (PYTHON_CMD     , REPEAT_COUNT, WARMPUP_COUNT)
    #runcsharp   (cs_exe         , REPEAT_COUNT, WARMPUP_COUNT)
    #runwincrypto(c_wincrypto_exe, REPEAT_COUNT, WARMPUP_COUNT)
    runperl     (PERL_CMD       , REPEAT_COUNT, WARMPUP_COUNT)

#----------------------
# MAIN
#----------------------
if __name__=="__main__":
    main()
