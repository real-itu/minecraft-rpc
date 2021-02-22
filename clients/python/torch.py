import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)



#client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
#    cube=Cube(
#        min=Point(x=-10, y=4, z=-10),
#        max=Point(x=10, y=14, z=10)
#    ),
#    type=AIR
#))
client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
    # Lower layer
    Block(position=Point(x=1, y=4, z=1), type=TORCH, orientation=SOUTH),
]))