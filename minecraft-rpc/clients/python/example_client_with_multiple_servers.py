from __future__ import print_function

import random
import logging

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

host = "18.196.132.177"

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
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=10000, minHeapSize=512))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())

    return servers

#Spawn server with docker
channel = grpc.insecure_channel(host+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

#Calls for async spawn of 2 servers
servers = spawnServers(client, 2)

print(servers)

for server in servers:
    #Establish connection to spawned server
    server1_channel = grpc.insecure_channel(host + ':'+str(server.rpcPort))
    server1_client = minecraft_pb2_grpc.MinecraftServiceStub(server1_channel)

    server1_client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
        cube=Cube(
            min=Point(x=-10, y=4, z=-10),
            max=Point(x=10, y=14, z=10)
        ),
        type=AIR
    ))
    server1_client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
        # Lower layer
        Block(position=Point(x=1, y=5, z=1), type=PISTON, orientation=NORTH),
        Block(position=Point(x=1, y=5, z=0), type=SLIME, orientation=NORTH),
        Block(position=Point(x=1, y=5, z=-1), type=STICKY_PISTON, orientation=SOUTH),
        Block(position=Point(x=1, y=5, z=-2), type=PISTON, orientation=NORTH),
        Block(position=Point(x=1, y=5, z=-4), type=SLIME, orientation=NORTH),
        # Upper layer
        Block(position=Point(x=1, y=6, z=0), type=REDSTONE_BLOCK, orientation=NORTH),
        Block(position=Point(x=1, y=6, z=-4), type=REDSTONE_BLOCK, orientation=NORTH),
        # Activate
        Block(position=Point(x=1, y=6, z=-1), type=QUARTZ_BLOCK, orientation=NORTH),
    ]))

    input("luk servers?")

    #client.CloseServer(Port(port=port.rpcPort))
