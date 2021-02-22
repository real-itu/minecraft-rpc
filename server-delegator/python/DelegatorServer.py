from concurrent import futures
import logging

import grpc

import delegator_pb2
import delegator_pb2_grpc


class Greeter(delegator_pb2_grpc.DelegatorService):

    def SayHello(self, request, context):
        return delegator_pb2.PortReply(port='hej')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delegator_pb2_grpc.add_DelegatorServiceServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()