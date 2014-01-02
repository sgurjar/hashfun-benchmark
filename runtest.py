import os, os.path, subprocess, platform

basedir=os.path.dirname(os.path.realpath(__file__))
datadir=os.path.join(basedir,'data')
srcdir =os.path.join(basedir,'source')

java_cmd='c:/tools/jdk/jdk1.7.0_25/bin/java.exe'
python_cmd='c:/tools/python/Python275/python.exe'

repeat_count='10'
warmpup_count='5'
hash_algorithms= ('md5','sha1','sha256','sha512')

datafiles=filter(lambda x: x.endswith('.dat'), os.listdir(datadir))

def platform_info():
    info={}
    if platform.system().lower().startswith('win'): # windows use wmic
        cpuinfo=dict(x.split('=',1) for x in subprocess.check_output('wmic cpu get name,caption,numberofcores /format:value'.split()).splitlines() if x)
        info['processor']=cpuinfo['Caption']
        info['cpu'      ]=cpuinfo['Name']
        info['cores'    ]=cpuinfo['NumberOfCores']
        osinfo = dict(x.split('=',1) for x in subprocess.check_output('wmic os get caption,osarchitecture,totalvisiblememorysize /format:value'.split()).splitlines() if x)
        info['os']=osinfo['Caption'] + osinfo['OSArchitecture']
        info['ram']=osinfo['TotalVisibleMemorySize']

    print '##',info['os']
    print '##',info['processor']
    print '##',info['cpu']+', #cores',info['cores']
    print '##','RAM',info['ram'],'bytes'

def runjava():
    #prefix=subprocess.check_output([java_cmd,'-version'])
    prefix='java'

    for datafile in datafiles:
        for algo in hash_algorithms:
            args = [ java_cmd,
                     '-cp', srcdir+'/java/build',
                     'testhashfuns',
                     repeat_count,
                     warmpup_count,
                     algo,
                     os.path.join(datadir,datafile)
                   ]
            for line in subprocess.check_output(args).splitlines():
                print 'java', algo, datafile, line

def runpython():
    #prefix=subprocess.check_output([python_cmd,'-V']).strip()
    prefix='python'

    for datafile in datafiles:
        for algo in hash_algorithms:
            args = [ python_cmd,
                     'source/python/testhashfuns.py',
                     repeat_count,
                     warmpup_count,
                     algo,
                     os.path.join(datadir,datafile)
                   ]
            for line in subprocess.check_output(args).splitlines():
                print prefix, algo, datafile, line

platform_info()
runjava()
runpython()