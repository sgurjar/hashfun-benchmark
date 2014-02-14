#
# http://stackoverflow.com/questions/21764293/perl-digest-add-addfile-computes-different-sha1-digest
#
use strict;
use warnings;
#use Digest::MD5 qw(md5);
#use Digest::SHA qw(sha1 sha1_hex sha256 sha512);
use Digest;
use Time::HiRes qw(time);

# read command line args
# ------------------------
(@ARGV >= 4) or die "usage: perl $0 repeatcount warmupcount algo datafile\n";
my ($repeatcount, $warmupcount, $algo, $datafile) = @ARGV;

my ($fh, $data, $hashfun, $hashval, $start_tm, $end_tm);

# get hash algo
# --------------
if    ($algo eq "md5"   ) { $hashfun = Digest->new("MD5"    );}
elsif ($algo eq "sha1"  ) { $hashfun = Digest->new("SHA-1"  );}
elsif ($algo eq "sha256") { $hashfun = Digest->new("SHA-256");}
elsif ($algo eq "sha512") { $hashfun = Digest->new("SHA-512");}
else {
    die "error: invalid algorithm '$algo'\n"
}

open($fh, "<", $datafile ) or die "error: Can't open '$datafile', $!\n";
binmode($fh);

# warmup
# ------
for (my $i=0; $i < $warmupcount; $i++) {
    seek($fh, 0, 0); # reset to the start
    $hashfun->addfile(*$fh);
    $hashval = $hashfun->digest();
}


# real
# ----
for (my $i=0; $i < $repeatcount; $i++) {
    seek($fh, 0, 0); # reset to the start
    $start_tm = time();
    $hashfun->addfile(*$fh);
    $hashval = $hashfun->digest();
    $end_tm  = time();
    print $i, " ", unpack('H*', $hashval), " ",
            int(($end_tm-$start_tm)*1000),"\n";
}

close($fh);

