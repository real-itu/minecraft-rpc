from __future__ import print_function

import random
import logging

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []

#Returns single layer of entities
def getSingleLayerOfEntities(x, y, z, size):
    layerOfEntities = []

    for i in range(size-1):
        for u in range(size-1):
            layerOfEntities.append(SpawnEntity(spawnPosition=Point(x=x+i, y=y, z=z+u), type=ENTITY_CREEPER))
    return layerOfEntities

#Returns single layer of blocks
def getSingleLayerOfBlocks(x, y, z, size):
    layerOfBlocks = []

    for i in range(size-1):
        for u in range(size-1):
            layerOfBlocks.append(Block(position=Point(x=x+i, y=y, z=z+u), type=DIRT,  orientation=NORTH))
    return layerOfBlocks

#Gives chunks of entities
def getChunkOfEntities(x, y, z, height, size):
    blocks = []
    for i in range(y, height, 3):
        blocks= blocks + getSingleLayerOfBlocks(x, i, z, size)
    
    entities = []
    for i in range(y, height, 3):
        entities = entities + getSingleLayerOfEntities(x, i, z, size)

    return (blocks, entities)

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
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())

    return servers

def spawnEntityChunkOnServer(servers, posX, posY, posZ, size):
    i = 0
    while i < len(servers):
        #Establish connection to spawned server
        server_channel = grpc.insecure_channel('localhost:'+str(servers[i].rpcPort))
        server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

        #Spawn lag machine on server
        blocks, entities = getChunkOfEntities(posX, posY, posZ, height, size)
        server_client.spawnBlocks(Blocks(blocks=blocks))
        server_client.spawnEntities(SpawnEntities(spawnEntities=entities))
        i +=1
    


posX = int(input("Where do you want your entity chunk? format: x ENTER y ENTER z ENTER\n"))
posY = int(input())
posZ = int(input())
height = int(input("How many layers of entities do you want? format: h\n"))
size = int(input("What should the size be of the entity chunk area? format: s\n"))
amountOfServers = int(input("How many servers do you want duplicated with these entity chunks? format: c\n"))

print("Processing ...")

#Make docker
channel = grpc.insecure_channel('localhost:5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

spawnEntityChunkOnServer(servers, posX, posY, posZ, size)