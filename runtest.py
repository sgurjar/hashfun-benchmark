#!/usr/bin/python

import sys, os, os.path, subprocess, platform

IS_WINDOWS = platform.system().lower().startswith('win')

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(BASEDIR,'data')
SRCDIR  = os.path.join(BASEDIR,'source')

JAVA_CMD   = 'c:/tools/jdk/jdk1.7.0_25/bin/java.exe' if IS_WINDOWS else 'java'
PYTHON_CMD = 'c:/tools/python/Python275/python.exe' if IS_WINDOWS else 'python'
PERL_CMD   = 'c:/tools/perl/strawberry/perl/bin/perl.exe' if IS_WINDOWS else 'perl'
RUBY_CMD   = 'c:/tools/ruby/ruby-2.0.0-p353-i386-mingw32/bin/ruby.exe' if IS_WINDOWS else 'ruby'

REPEAT_COUNT    = '10'
WARMPUP_COUNT   = '5'

HASH_ALGORITHMS = ('md5', 'sha1', 'sha256', 'sha512')

DATAFILES       = filter(lambda x: x.endswith('.dat'), os.listdir(DATADIR))
#DATAFILES       = ['0002mb.dat']



#----------------------
def platform_info():
    info={}
    if IS_WINDOWS: # windows use wmic

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
    else:   # linux
        pass

#----------------------
def runtest(**kwargs):
    for datafile in DATAFILES:
        for algo in HASH_ALGORITHMS:
            try:
                for line in subprocess.check_output(
                        kwargs['getargs'](algo, datafile)).splitlines():
                    print kwargs['prefix'], algo, datafile, line
            except subprocess.CalledProcessError as e:
                print e.cmd, e.output

#----------------------
#java -server -XX:+UseG1GC -Xms$heapsize -Xmx$heapsize -XX:MaxGCPauseMillis=500 \
#-cp source/java/build/ testhashfuns $repeatcount $warmupcount sha512 data/0004mb.dat

def runjava(java_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ java_cmd,
                 '-server', 
                 '-XX:+UseG1GC', '-XX:MaxGCPauseMillis=500',
                 '-Xms1152M', '-Xmx1152M',
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
def runopenssl(cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ cmd,
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='c_openssl', getargs=getargs)

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
def runruby(ruby_cmd, repeat_count, warmpup_count):
    def getargs(algo, datafile):
        return [ ruby_cmd,
                 'source/ruby/testhashfuns.rb',
                 repeat_count,
                 warmpup_count,
                 algo,
                 os.path.join(DATADIR,datafile)
               ]

    runtest(prefix='ruby', getargs=getargs)

#----------------------
def verify_digest():
    a={}
    for line in sys.stdin.readlines():
        #print line.strip()
        if not line.startswith('##'):
            (lang, algo, datafile, index, digest, elapsed) = line.split()
            a.setdefault(lang + '-' + algo + '-' + datafile, []).append(digest)

    b={}
    for k in sorted(a.keys()):
        (lang, algo, data) = k.split('-')
        if (algo+'-'+data) in b:
            if b[algo+'-'+data] != a[k]:
                print "digest mismatch: %s %s %s" % (lang, algo, data)
                print "actual   %s" % a[k]
                print "expected %s" % b[algo+'-'+data]
                return
        else:
            b[algo+'-'+data] = a[k]

"""
def analyze_this():
    import itertools

    header = ('lang','algo','datafile','rindex','digest','elapsed')

    data = sys.stdin.readlines()
    data = itertools.ifilter(lambda x: x and not x.startswith('#'), data)
    data = itertools.imap(lambda x: dict(zip(header, x.split())), data)
    grp_by_lang_algo_data = itertools.groupby(
                    data, key=lambda x:x['lang']+'-'+x['algo']+'-'+x['datafile'])

    # from repeatcount runs find the one that took min elapsed time
    grp_by_lang_algo_data_minelapsed = itertools.imap (
       lambda (a,b) : min( b, key=lambda x: int(x['elapsed']) ),
       grp_by_lang_algo_data )

    plot(itertools.ifilter(lambda x: x['lang']=='ruby',
                            grp_by_lang_algo_data_minelapsed))


def plot(data):
    import numpy as np
    import matplotlib.pyplot as plt
    import itertools, re

    data = list(data)

    md5 = filter(lambda x: x['algo']=='md5', data)
    dtf = map(lambda x: re.sub(r'\.dat$','',re.sub(r'^0*','',x)),
                            map(lambda x:x['datafile'], md5))

    etm = map(lambda x:int(x['elapsed']), md5)
    ind = np.arange(len(etm))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, etm, width, color='r') # , yerr=menStd

    #---------
    sha1 = filter(lambda x: x['algo']=='sha1', data)
    dtf = map(lambda x: re.sub(r'\.dat$','',re.sub(r'^0*','',x)),
                            map(lambda x:x['datafile'], sha1))

    etm = map(lambda x:int(x['elapsed']), sha1)
    ind = np.arange(len(etm)) + width
    rects2 = ax.bar(ind, etm, width, color='y') # , yerr=menStd

    #---------
    sha256 = filter(lambda x: x['algo']=='sha256', data)
    dtf = map(lambda x: re.sub(r'\.dat$','',re.sub(r'^0*','',x)),
                            map(lambda x:x['datafile'], sha256))

    etm = map(lambda x:int(x['elapsed']), sha256)
    ind = np.arange(len(etm)) + width + width
    rects3 = ax.bar(ind, etm, width, color='b') # , yerr=menStd

    ax.set_ylabel('Milliseconds')
    ax.set_title('Ruby')
    ax.set_xticks(ind + width + width)
    ax.set_xticklabels(dtf)

    #ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

    plt.show()

"""

#----------------------
def main():
    platform_info()

    runjava  (JAVA_CMD  , REPEAT_COUNT, WARMPUP_COUNT)
    runpython(PYTHON_CMD, REPEAT_COUNT, WARMPUP_COUNT)
    runperl  (PERL_CMD  , REPEAT_COUNT, WARMPUP_COUNT)
    runruby  (RUBY_CMD  , REPEAT_COUNT, WARMPUP_COUNT)
    runopenssl('source/c/testhashfuns_openssl', REPEAT_COUNT, WARMPUP_COUNT)

    if IS_WINDOWS:    
        cs_exe          = 'source/c#/testhashfuns_cs.exe'
        c_wincrypto_exe = 'source/c/testhashfuns_win32crypto.exe'
        runcsharp   (cs_exe         , REPEAT_COUNT, WARMPUP_COUNT)
        runwincrypto(c_wincrypto_exe, REPEAT_COUNT, WARMPUP_COUNT)

#----------------------
# MAIN
#----------------------
if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1]=='-v': verify_digest()
        #elif sys.argv[1]=='-a': analyze_this()
    else:
        main()
