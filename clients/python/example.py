import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

response = client.spawnBlocks(Blocks(blocks=[
    Block(position=Point(x=1, y=5, z=1), type=QUARTZ_BLOCK, orientation=NORTH),
    Block(position=Point(x=2, y=5, z=1), type=OBSIDIAN, orientation=UP)
]))
print(response)

response = client.readCube(Cube(min=Point(x=1, y=1, z=1), max=Point(x=2, y=3, z=3)))
print(response)

response = client.fillCube(FillCubeRequest(
    volume=Cube(min=Point(x=1, y=8, z=1), max=Point(x=2, y=9, z=3)),
    type=OBSIDIAN
))
print(response.status)
