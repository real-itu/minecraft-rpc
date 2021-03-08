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

blockClusters = []

s = input("How many clusters: ")

for c in range(int(s)):
    blockList = []
    for i in range(20):
        for r in range(20):
            for l in range(20):
                blockList.append(Block(position=Point(x=(c*20+i+c)-560, y=l+5, z=r+2000), type=DIRT, orientation=NORTH))
    blockClusters.append(blockList)

print("start")
for x in blockClusters:
    server1_client.spawnBlocks(Blocks(blocks=x))
print("over")

#client.CloseServer(Port(port=port.rpcPort))

print(port)

