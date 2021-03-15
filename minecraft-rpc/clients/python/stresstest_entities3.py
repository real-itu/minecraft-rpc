from __future__ import print_function

import random
import logging
import time

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

servers = []
ip = "localhost"

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
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=6000))
        futures.append(call_future)

    futures = wait_for_futures(futures)

    for i in range(len(futures)):
        servers.append(futures[i].result())

    return servers
    
def sendCommand(server, cmd):
    server_channel = grpc.insecure_channel(ip+':'+str(server.rpcPort))
    server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

    server_client.executeCommands(Commands(commands=[
        Command(command=cmd)
    ]))

#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
def getEntityColumn(x, y, z):
    height = y
    cap = 256
    blocks = []
    entities = []
    
    while height < cap:
        entities.append(SpawnEntity(spawnPosition=Point(x=x, y=height+1, z=z), type=ENTITY_CREEPER))
        blocks.append(Block(position=Point(x=x, y=height, z=z, type=DIRT, orientation=NORTH)))
        blocks.append(Block(position=Point(x=x, y=height+1, z=z, type=AIR, orientation=NORTH)))
        blocks.append(Block(position=Point(x=x, y=height+2, z=z, type=AIR, orientation=NORTH)))
        height += 3

    return blocks, entities


def getEntities(x, y, z, size):
    blocks = []
    entities = []

    for i in range(size):
        cBlocks, cEntities = getEntityColumn(x+((i)%16), y, z+((i)/16))
        blocks += cBlocks
        entities += cEntities


    return blocks, entities


def spawnEntities(servers, posX, posY, posZ, size):
    i = 0
    while i < len(servers):
        #Establish connection to spawned server
        server_channel = grpc.insecure_channel(ip+':'+str(servers[i].rpcPort))
        server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

        #Spawn lag machine on server
        blocks, entities = getEntities(posX, posY, posZ, size)
        server_client.spawnBlocks(Blocks(blocks=blocks))
        server_client.spawnEntities(SpawnEntities(spawnEntities=entities))
        i +=1


#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#


posX = int(input("Where do you want your entity chunk? format: x ENTER y ENTER z ENTER\n"))
posY = int(input())
posZ = int(input())
size = int(input("How many?\n"))
amountOfServers = int(input("How many servers do you want duplicated with these entity chunks? format: c\n"))

print("Entities: ", (256-posY)/3*size)
print("Processing ...")

#Make docker
channel = grpc.insecure_channel(ip+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

spawnEntities(servers, posX, posY, posZ, size)

while 1:
    time.sleep(2)
    for server in servers:
        sendCommand(server, "sponge tps")