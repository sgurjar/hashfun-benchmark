use strict;
use warnings;
use Digest::MD5 qw(md5);
use Digest::SHA qw(sha1 sha256 sha512);
use Time::HiRes qw(time);

# read command line args
# ------------------------
(@ARGV >= 4) or die "usage: perl $0 repeatcount warmupcount algo datafile\n";
my ($repeatcount, $warmupcount, $algo, $datafile) = @ARGV;

my ($data, $hashfun, $hashval, $start_tm, $end_tm);

# read data file
# --------------
open( my $fh, "<", $datafile ) or die "error: Can't open '$datafile', $!\n";
binmode $fh;
read($fh, $data, -s $datafile);
close($fh);

# get hash algo
# --------------
if    ($algo eq "md5"   ) { $hashfun = \&md5   ; }
elsif ($algo eq "sha1"  ) { $hashfun = \&sha1  ; }
elsif ($algo eq "sha256") { $hashfun = \&sha256; }
elsif ($algo eq "sha512") { $hashfun = \&sha512; }
else {
    die "error: invalid algorithm '$algo'\n"
}

# warmup
# ------
for (my $i=0; $i < $warmupcount; $i++) {
    $hashval = $hashfun->($data);
}

# real
# ----
for (my $i=0; $i < $repeatcount; $i++) {
    $start_tm = time();
    $hashval  = $hashfun->($data);
    $end_tm   = time();
    print $i, " ", unpack('H*', $hashval), " ",
            int(($end_tm-$start_tm)*1000),"\n";
}