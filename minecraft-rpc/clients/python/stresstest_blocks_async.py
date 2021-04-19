from __future__ import print_function

import time
import sys

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []
#ip = "3.65.20.197"
ip = sys.argv[4]

x = 100
y = 3 
z = 100

#Waits for all futures in a list to be done
def wait_for_futures(futures):
    b = True
    while(b):
        b = False
        for i in futures:
            if(not i.done()): b = True
    return futures

#Async calls the spawning of servers
def spawnServers(client, amount):
    futures = []
    servers = []

    for i in range(amount):
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=10240))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())
    return servers

def sendCommand(c, cmd):
    #server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    #server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    c.executeCommands(Commands(commands=[
        Command(command=cmd)
    ]))

def sendCommandToServer(se, cmd):
    server_channel = grpc.insecure_channel(ip+':'+str(se.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    server_client.executeCommands(Commands(commands=[
        Command(command=cmd)
    ]))

#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
def asyncSpawnCubesOnServers(servers, cubes, blockType, t):
    futures = []
    clients = []
    for s in servers:
        server_channel = grpc.insecure_channel(ip+':'+str(s.rpcPort))
        clients.append(minecraft_pb2_grpc.MinecraftServiceStub(server_channel))
    
    if(t): start = time.perf_counter()
    for c in clients:
        sendCommand(c, "say "+ str(n))
        for cu in cubes:
            call_future = c.fillCube.future(FillCubeRequest(
                cube=cu,
                type=blockType
            ))
            futures.append(call_future)


        #futures.append(call_future)

    wait_for_futures(futures)
    if(t):
        took = time.perf_counter() - start
        print(took)

    

amountOfServers = int(sys.argv[1])
cubesCount = int(sys.argv[2])
nmax = int(sys.argv[3])

#amountOfServers = int(input("How many servers?\n"))
#cubesCount = int(input("How many cubes pr. server? \n"))


#Make docker
channel = grpc.insecure_channel(ip+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

#Prints the server ports for grpc calls and minecraft connects
for i in range(len(servers)):
    print("Server "+str(i)+": ")
    print(servers[i])

b = True
n = 1
try:
    while n < nmax:
        cube1 = Cube(min=Point(x=x+1, y=y, z=z+1), max=Point(x=x+1+(n-1), y=y+n-1, z=z+1+(n-1)))
        cube2 = Cube(min=Point(x=x-1, y=y, z=z-1), max=Point(x=x-1-(n-1), y=y+n-1, z=z-1-(n-1)))
        cube3 = Cube(min=Point(x=x-1, y=y, z=z+1), max=Point(x=x-1-(n-1), y=y+n-1, z=z+1+(n-1)))
        cube4 = Cube(min=Point(x=x+1, y=y, z=z-1), max=Point(x=x+1+(n-1), y=y+n-1, z=z-1-(n-1)))


        cubes = []
        if(cubesCount == 1): cubes = [cube1]
        if(cubesCount == 2): cubes = [cube1, cube2]
        if(cubesCount == 3): cubes = [cube1, cube2, cube3]
        if(cubesCount == 4): cubes = [cube1, cube2, cube3, cube4]
        print(n)
        asyncSpawnCubesOnServers(servers, cubes, OBSIDIAN, True)
        asyncSpawnCubesOnServers(servers, cubes, AIR, False)
        n += 1
except:
    print(sys.exc_info()[0])

for server in servers:
    sendCommandToServer(server, "stop")
time.sleep(2)
