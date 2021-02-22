from __future__ import print_function
import logging

import grpc

import delegator_pb2
import delegator_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:5001') as channel:
        stub = delegator_pb2_grpc.DelegatorServiceStub(channel)
        response = stub.spawnServer(delegator_pb2.Port(port='111'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()