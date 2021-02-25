from concurrent import futures
import time
import math
import logging
import docker
import socket

import grpc

import delegator_pb2
import delegator_pb2_grpc

class DelegatorServicer(delegator_pb2_grpc.DelegatorServicer):
    def SpawnNewServer(self, request, context):
        client = docker.from_env()
        sock = socket.socket()
        sock.bind(('',0))
        _, port = sock.getsockname()
        sock.close()
        container = client.containers.run("mc-server:latest", detach=True, ports={'5001/tcp':str(port), '25565/tcp':'25565'})
        portMessage = delegator_pb2.Port(port=port)
        return portMessage

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delegator_pb2_grpc.add_DelegatorServicer_to_server(
        DelegatorServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

serve()