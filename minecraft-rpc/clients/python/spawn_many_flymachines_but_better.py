import sys
import os

servers = int(sys.argv[1])
start = int(sys.argv[2])
step = int(sys.argv[3])
end = int(sys.argv[4])
ip = sys.argv[5]

for i in range(start, end, step):
    os.system(f"py stresstest_flyingmachines.py {servers} {i} {ip}")