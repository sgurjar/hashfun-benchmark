import sys, hashlib, time

repeatCount = int(sys.argv[1])
warmupCount = int(sys.argv[2])
algoname    = sys.argv[3]
datafileName= sys.argv[4]

f = open(datafileName,'rb')
data = f.read()
f.close()

algos = {
    'md5'   : hashlib.md5,
    'sha1'  : hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha512': hashlib.sha512
}

hashfun = algos.get(algoname)

if not hashfun:
    raise Exception('invalid alogrithm %s' % algoname)

for i in range(warmupCount):
    hashfun(data).digest()

for i in range(repeatCount):
    start = time.clock()
    digest = hashfun(data).hexdigest()
    end = time.clock()
    print i, digest, int((end-start)*1000)
