from __future__ import print_function

import random
import logging

import grpc
import asyncio

from delegator_pb2 import *
import delegator_pb2_grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

#Spawn server with docker
channel = grpc.insecure_channel('localhost:5001')
client = delegator_pb2_grpc.DelegatorStub(channel)

fut = client.SpawnNewServer.future(ServerConfig(worldType=FLAT))
fut.wait()

