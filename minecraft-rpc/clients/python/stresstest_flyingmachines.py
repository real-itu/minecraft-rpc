from __future__ import print_function

import time
import sys

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []
#ip = "35.158.138.94"
ip = sys.argv[3]

x = 50
y = 5 
z = 50

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

def getFlyingMachine(x, y, z):
    blocks = []
    blocks.append(Block(position=Point(x=x, y=y, z=z), type=PISTON, orientation=NORTH))
    blocks.append(Block(position=Point(x=x, y=y, z=z-1), type=SLIME, orientation=NORTH))
    blocks.append(Block(position=Point(x=x, y=y, z=z-2), type=STICKY_PISTON, orientation=SOUTH))
    blocks.append(Block(position=Point(x=x, y=y, z=z-3), type=PISTON, orientation=NORTH))
    blocks.append(Block(position=Point(x=x, y=y, z=z-5), type=SLIME, orientation=NORTH))
    # Upper layer
    blocks.append(Block(position=Point(x=x, y=y+1, z=z-1), type=REDSTONE_BLOCK, orientation=NORTH))
    blocks.append(Block(position=Point(x=x, y=y+1, z=z-5), type=REDSTONE_BLOCK, orientation=NORTH))
    # Activate
    blocks.append(Block(position=Point(x=x, y=y+1, z=z-2), type=QUARTZ_BLOCK, orientation=NORTH))
    return blocks

def spawnBlocks(server, machines):
    #Establish connection to spawned server
    server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    server_client.spawnBlocks(Blocks(blocks=machines))


sys.argv

#amountOfServers = int(input("How many servers do you want?\n"))
#n = int(input("How many flying machines pr. server? \n"))
amountOfServers = int(sys.argv[1])
print(int(sys.argv[1]))
n = int(sys.argv[2])
print(int(sys.argv[2]))

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



flyingMachines = []
u = 0
while u < n*2:
    flyingMachines += getFlyingMachine(x+u, y,z)
    u +=2

nr = 0
for server in servers:
    spawnBlocks(server, flyingMachines)
    sendCommand(server, "I AM SERVER: "+str(nr))
    sendCommand(server, "AMOUNT OF FLYING MACHINES: "+str(n))
    nr += 1;


b = True
start = time.perf_counter()
while b:
    for server in servers:
        sendCommand(server, "sponge tps")


    took = time.perf_counter() - start
    if(took > 21): b = False
for server in servers:
    sendCommand(server, "stop")

time.sleep(1)