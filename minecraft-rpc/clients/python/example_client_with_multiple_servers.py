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

#client.CloseServer(Port(port=port.rpcPort))

print(port)

