from __future__ import print_function
import grpc

#Add import location for necessary files
import sys
sys.path.insert(1, '../../server')


import delegator_pb2_grpc
from delegator_pb2 import *

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
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------#

amountOfServers = int(input("How many servers do you want? \n"))\

#Make docker
channel = grpc.insecure_channel(ip+':5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

servers = []
servers = spawnServers(client, amountOfServers)

#Prints the server ports for grpc calls and minecraft connects
for i in range(len(servers)):
    print("Server "+str(i)+": ")
    print(servers[i])

#Simple while loop for closing servers
b=1
while b==1:
    i = input("Press 's' to stop all servers \n")
    if i=='s':
        for server in servers:
            client.CloseServer(Port(port=server.rpcPort))
        b=0