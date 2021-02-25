from __future__ import print_function

import random
import logging

import grpc

import test_pb2
import test_pb2_grpc

channel = grpc.insecure_channel('localhost:5001')
stub = test_pb2_grpc.DelegatorStub(channel)

color = stub.GetColorOf(test_pb2.Block(type="blue"))

#color_future = stub.GetColorOf.future(test_pb2.Block(color="blue"))
#newcolor = color_future.result()

print(color)
print("-----------")
#print(newcolor)
