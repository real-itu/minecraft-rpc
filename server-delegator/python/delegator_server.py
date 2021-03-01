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
defaultImage = "fred5229/evocraft_minecraft_server:default"
flatImage = "fred5229/evocraft_minecraft_server:flat"
docker_client.images.pull(defaultImage)
docker_client.images.pull(flatImage)


containers = {}


class DelegatorServicer(delegator_pb2_grpc.DelegatorServicer):
    def SpawnNewServer(self, request, context):

        rpcSock = socket.socket()
        mcSock = socket.socket()
        rpcSock.bind(('',0))
        mcSock.bind(('',0))
        _, rpcPort1 = rpcSock.getsockname()
        _, mcPort1 = mcSock.getsockname()
        rpcSock.close()
        mcSock.close()

        imageName = ''
        if request.worldType == delegator_pb2.WorldType.FLAT:
            imageName = flatImage
        elif request.worldType == delegator_pb2.WorldType.DEFAULT:
            imageName = defaultImage
        container = docker_client.containers.run(imageName, detach=True, ports={'5001/tcp':str(rpcPort1), '25565/tcp':str(mcPort1)})
        containers[rpcPort1] = container

        portMessage = delegator_pb2.Ports(rpcPort=rpcPort1, mcPort=mcPort1)
        return portMessage

    def CloseServer(self, request, context):
        containers[request.port].stop()
        return delegator_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delegator_pb2_grpc.add_DelegatorServicer_to_server(
        DelegatorServicer(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()

serve()