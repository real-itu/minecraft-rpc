import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

#client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
#    # Lower layer
#    Block(position=Point(x=17001, y=5, z=1), type=PISTON, orientation=NORTH),
#    Block(position=Point(x=17001, y=5, z=0), type=SLIME, orientation=NORTH),
#    Block(position=Point(x=17001, y=5, z=-1), type=STICKY_PISTON, orientation=SOUTH),
#    Block(position=Point(x=17001, y=5, z=-2), type=PISTON, orientation=NORTH),
#    Block(position=Point(x=17001, y=5, z=-4), type=SLIME, orientation=NORTH),
#    # Upper layer
#    Block(position=Point(x=17001, y=6, z=0), type=REDSTONE_BLOCK, orientation=NORTH),
#    Block(position=Point(x=17001, y=6, z=-4), type=REDSTONE_BLOCK, orientation=NORTH),
#    # Activate
#    Block(position=Point(x=17001, y=6, z=-1), type=QUARTZ_BLOCK, orientation=NORTH),
#]))

client.spawnEntities(SpawnEntities(spawnEntities=[
    SpawnEntity(type=ENTITY_FURNACE_MINECART, spawnPosition=Point(x=50000, y=5, z=50000))
]))

input("read?")

ents = client.readEntitiesInSphere(Sphere(center=Point(x=50000, y=5, z=50000), radius=5.0))

#cubes = client.readCube(Cube(min=Point(x=17000, y=5, z=-5), max=Point(x=17001, y=6, z=2)))

print(ents)