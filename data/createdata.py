#!/usr/bin/env python
import os

file_sizes_in_mb=(
2,
4,
8,
16,
32,
64,
128,
256,
512,
640,
768,
896,
1024)

def create_rnd_file(size_in_mb, filename):
    with open(filename,'wb') as f:
        f.write(os.urandom(size_in_mb*1024*1024))

for mb in file_sizes_in_mb:
    create_rnd_file(mb, '%04dmb.dat'%mb)
