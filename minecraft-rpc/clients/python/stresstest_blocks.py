from __future__ import print_function

import time

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []
ip = "3.127.139.46"

x = 100
y = 6 
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
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=6000))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())
    return servers

def sendCommand(server, cmd):
    server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    server_client.executeCommands(Commands(commands=[
        Command(command=cmd)
    ]))

#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
timeSamples = []

def spawnCubesOnServer(server, cubes, blockType, t):
    #Establish connection to spawned server
    server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    #Spawn cube
    cTook = 0
    for c in cubes:
        #if(t): start = time.perf_counter()
        server_client.fillCube(FillCubeRequest(
            cube=c,
            type=blockType
        ))
        #if(t): 
        #    took = time.perf_counter()-start
        #    cTook += took
    #if(t):
    #    timeSamples.append(cTook)
    #    print(cTook)


amountOfServers = int(input("How many servers do you want duplicated with these lag machines? format: c\n"))
cubesCount = int(input("How many cubes pr. server? \n"))

print("Processing ...")

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
while n < 3:
    cube1 = [Cube(min=Point(x=x+1, y=y, z=z+1), max=Point(x=x+1+(n-1), y=y+n-1, z=z+1+(n-1)))]
    cube2 = [Cube(min=Point(x=x-1, y=y, z=z-1), max=Point(x=x-1-(n-1), y=y+n-1, z=z-1-(n-1)))]
    cube3 = [Cube(min=Point(x=x-1, y=y, z=z+1), max=Point(x=x+1+(n-1), y=y+n-1, z=z-1-(n-1)))]
    cube4 = [Cube(min=Point(x=x+1, y=y, z=z-1), max=Point(x=x-1-(n-1), y=y+n-1, z=z+1+(n-1)))]

    cubes = []
    if(cubesCount == 1): cubes = [cube1]
    if(cubesCount == 2): cubes = [cube1, cube2]
    if(cubesCount == 3): cubes = [cube1, cube2, cube3]
    if(cubesCount == 4): cubes = [cube1, cube2, cube3, cube4]
    print(len(cubes))
    print(cubesCount)
    for server in servers:
        sendCommand(server, "say "+ str(n))
        spawnCubesOnServer(server, cubes, OBSIDIAN, True)
        #spawnCubesOnServer(server, cubes, AIR, False)
    n += 1
