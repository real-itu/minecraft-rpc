from concurrent import futures
import time
import math
import logging
import docker
import socket

import grpc

import delegator_pb2
import delegator_pb2_grpc

docker_client = docker.from_env()
imageName = "fred5229/evocraft_minecraft_server:default"
docker_client.images.pull(imageName)

containers = {}


class DelegatorServicer(delegator_pb2_grpc.DelegatorServicer):
    def SpawnNewServer(self, request, context):
        docker_client = docker.from_env()
        rpcSock = socket.socket()
        mcSock = socket.socket()
        rpcSock.bind(('',0))
        mcSock.bind(('',0))
        _, rpcPort = rpcSock.getsockname()
        _, mcPort = mcSock.getsockname()
        rpcSock.close()
        mcSock.close()
        container = docker_client.containers.run(imageName, detach=True, ports={'5001/tcp':str(rpcPort), '25565/tcp':str(mcPort)})
        containers[rpcPort] = container

        portMessage = delegator_pb2.Ports(rpcPort=rpcPort, mcPort=mcPort)
        return portMessage

    def CloseServer(self, request, context):
        containers[request.port].close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delegator_pb2_grpc.add_DelegatorServicer_to_server(
        DelegatorServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

serve()