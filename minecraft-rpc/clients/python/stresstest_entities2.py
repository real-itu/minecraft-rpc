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
        call_future = client.SpawnNewServer.future(ServerConfig(worldType=FLAT, maxHeapSize=3000))
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

def getEntities(x, y, z, size):
    entities = []
    for i in range(size):
        entities.append(SpawnEntity(spawnPosition=Point(x=x, y=y, z=z), type=ENTITY_CREEPER))
    return entities


def spawnEntities(servers, posX, posY, posZ, size):
    i = 0
    while i < len(servers):
        #Establish connection to spawned server
        server_channel = grpc.insecure_channel(ip+':'+str(servers[i].rpcPort))
        server_client = minecraft_pb2_grpc.MinecraftServiceStub(server_channel)

        #Spawn lag machine on server
        entities = getEntities(posX, posY, posZ, size)
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

print("Processing ...")

#Make docker
channel = grpc.insecure_channel(ip+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

spawnEntities(servers, posX, posY, posZ, size)

while 1:
    time.sleep(5)
    for server in servers:
        sendCommand(server, "sponge tps")