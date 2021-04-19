import sys
import os

servers = int(sys.argv[1])
cubes = int(sys.argv[2])
nmax = int(sys.argv[3])
ip = sys.argv[4]

for i in range(3):
    os.system(f"py stresstest_blocks_v2.py {servers} {cubes} {nmax} {ip} > ./output/blocks({servers}servers_{cubes}cubes_{nmax}n)_{i}.txt")
