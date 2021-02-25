from concurrent import futures
import time
import math
import logging

import grpc

import test_pb2
import test_pb2_grpc

class DelegatorServicer(test_pb2_grpc.DelegatorServicer):
    def GetColorOf(self, request, context):
        color = test_pb2.Color(color=request.type)
        return color

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_DelegatorServicer_to_server(
        DelegatorServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

serve()