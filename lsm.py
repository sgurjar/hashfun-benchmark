
#
# least square mean
# based on AEF's spreadsheet
#
# in our case x would datasize
# and y would be avg resp time
# for a given language and algo
#
def compute_a_and_b(x, y):
    assert len(x)==len(y)
    n = len(x) # number of observations

    D = sum(x)
    E = sum(y)
    G = sum( map(lambda x,y: x*y, x, y) )
    H = sum( map(lambda x,y: x*y, x, x) )
    I = n * G
    J = D * E
    K = I - J
    L = n * H
    M = D * D
    N = L - M
    b = K / N
    P = b * D
    Q = E - P
    a = Q / n

    return round(a,3), round(b,3)
#
# y = a + bx
def a_plus_bx(a, b, X):
    return [(x, a + (b * x)) for x in X]

def lsm_y(x, y):
    (a,b) = compute_a_and_b(x, y)
    return a_plus_bx(a, b, x)

#
# plot x and y
def plotxy(x, y, **kwargs):
    assert len(x) > 0 and len(y) > 0

    import matplotlib.pyplot as plt, numpy

    if isinstance(y[0],list) or isinstance(y[0],tuple):
        # we have multiple y
        for y_i in y: plt.plot(x, y_i, 'x-')
    else: # we have one y
        plt.plot(x, y)

    plt.title(kwargs.get('title'))
    plt.xlabel(kwargs.get('xlabel'))
    plt.ylabel(kwargs.get('ylabel'))
    plt.grid()

    if kwargs.get('save'):
        plt.savefig(kwargs.get('save'),
            bbox_inches='tight',
            transparent = True)

    plt.show()

def analyzeit(resultfile):
    import sqlite3

    with sqlite3.connect(':memory:') as c:

        c.execute("""create table mydata (
                                                lang,
                                                algo,
                                                size    integer,
                                                i       integer,
                                                digest,
                                                elapsed integer
                                           )""")

        with open(resultfile) as f:
            for rec in f.readlines():
                rec = rec.split()
                rec[2] = int(rec[2].replace('mb.dat','')) # size col
                c.execute("""insert into mydata(
                                                    lang,
                                                    algo,
                                                    size,
                                                    i,
                                                    digest,
                                                    elapsed
                                                    )
                              values(?, ?, ?, ?, ?, ?)""", rec)

        c.execute("""create table mydata_avg as
                        select lang,
                                algo,
                                size,
                                avg(elapsed) avg,
                                max(elapsed) max,
                                min(elapsed) min
                        from mydata
                        group by lang, algo, size""")

        algos = c.execute("select distinct algo from mydata_avg")
        algos = map(lambda x:x[0], algos)

        langs = c.execute('select distinct lang from mydata_avg')
        langs = map(lambda x:x[0], langs)

        sizes = c.execute('select distinct size from mydata_avg')
        sizes = map(lambda x:x[0], sizes)

        LG = {  'c_openssl' :'c',
                'java'      :'Java',
                'perl'      :'Perl',
                'python'    :'Python',
                'ruby'      :'Ruby'
             }


        # print averages in the format easy plot on excel
        # for each algo
        #    #algo   MB      c       Java    Perl    Python  Ruby
        #    sha512  2       19.0    71.3    72.1    18.5    18.9
        #    sha512  4       38.0    143.8   140.0   37.5    38.0
        #    sha512  8       77.0    286.0   288.0   75.5    75.1
        #    sha512  16      153.0   571.8   577.0   152.4   152.1
        #    sha512  32      303.0   1144.3  1154.4  303.5   303.1
        #    sha512  64      611.0   2292.3  2250.0  611.5   606.2
        #    sha512  128     1221.0  4569.3  4673.0  1223.6  1223.0
        #    sha512  256     2431.0  9154.7  9236.0  2448.4  2447.1
        #    sha512  512     4870.0  18283.1 18541.3 4864.3  4890.6
        #    sha512  640     6079.0  22770.2 22756.5 6123.4  6092.4
        #    sha512  768     7335.0  27347.4 27713.4 7335.4  7341.4
        #    sha512  896     8565.0  31964.3 32411.1 8572.4  8629.9
        #    sha512  1024    9812.0  36527.3 36901.2 9784.7  9713.5

        for algo in algos:
            tmp_table = 'mydata_avg_by_' + algo
            c.execute("""create table %s as
                            select *
                            from mydata_avg
                            where algo=?""" % tmp_table, (algo,))

            print '\t'.join(['#algo','MB'] + map(lambda x:LG[x], langs))

            for sz in sizes:
                avgs=[]
                for lang in langs:
                    avg = c.execute("select avg from %s where size=? and lang=?"
                                                        % tmp_table, (sz, lang))
                    avg = map(lambda x:x[0], avg)
                    assert len(avg) == 1
                    avgs.append(avg[0])

                print '\t'.join(
                                [algo, str(sz)] + # .replace('mb.dat','')
                                map(lambda x:str(x),avgs)
                            )

        # compute coffecients a and b in the equations y = a + bx
        #       #lang   algo    a       b
        #       c       md5     0.209   2.752
        #       Python  md5     -0.575  2.758
        #       Ruby    md5     -0.488  2.758
        #       Perl    md5     2.172   4.328
        #       Java    md5     -1.642  5.558
        print '\n'
        c.execute("create table mydata_ab (lang, algo, a real, b real)")
        a_and_b=[]
        for lang in langs:
            for algo in algos:
                
                x = c.execute("""select size 
                                    from mydata_avg 
                                    where lang=? and algo=? 
                                    order by size""",(lang,algo))
                y = c.execute("""select avg 
                                    from mydata_avg 
                                    where lang=? and algo=? 
                                    order by size""",(lang,algo))
                # make sure x and y are float
                x = map(lambda t: float(t[0]), x)
                y = map(lambda t: float(t[0]), y)
                (a, b) = compute_a_and_b(x, y)
                c.execute("""insert into mydata_ab(lang, algo, a, b) 
                            values(?, ?, ?, ?)""",(LG[lang], algo, a, b))
        
        print '\t'.join(('#lang','algo','a','b'))
        for a in c.execute("""select lang, algo, a, b 
                                from mydata_ab 
                                order by algo, b, a"""):
            print '\t'.join(map(lambda x:str(x), a))


analyzeit('ubuntu_results.txt')