import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
    # Lower layer
    Block(position=Point(x=1, y=4, z=1), type=DIRT, orientation=NORTH),
   # Block(position=Point(x=2, y=4, z=1), type=REDSTONE_TORCH, orientation=NORTH),
]))

x=client.readCube(Cube(min=Point(x=0,y=0,z=0), max=Point(x=2,y=6,z=2)))

print(x)