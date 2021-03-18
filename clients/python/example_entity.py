import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.spawnEntities(SpawnEntities(spawnEntities=[
    SpawnEntity(type=ENTITY_FURNACE_MINECART, spawnPosition=Point(x=700, y=5, z=700))
]))