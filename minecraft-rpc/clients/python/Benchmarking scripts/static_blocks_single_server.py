from __future__ import print_function

import random
import logging

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

#Spawn server with docker
channel = grpc.insecure_channel('localhost:5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

port = client.SpawnNewServer(ServerConfig(worldType=FLAT))

#Establish connection to spawned server
server1_channel = grpc.insecure_channel('localhost:'+str(port.rpcPort))
server1_client = minecraft_pb2_grpc.MinecraftServiceStub(server1_channel)

blockList = []

for i in range 1..100:
    for r in range 1..100:
        for l in range 5..105:
            blockList.append(Block(position=Point(x=i-560, y=l, z=r+2000), type=DIRT, orientation=NORTH))


server1_client.spawnBlocks(Blocks(blocks=blockList))

#client.CloseServer(Port(port=port.rpcPort))

print(port)

