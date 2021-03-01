from __future__ import print_function

import random
import logging

import grpc

from delegator_pb2 import *
import delegator_pb2_grpc

channel = grpc.insecure_channel('localhost:5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

port = client.SpawnNewServer(ServerConfig(worldType=FLAT))

client.CloseServer(Port(port=port.rpcPort))

print(port)

