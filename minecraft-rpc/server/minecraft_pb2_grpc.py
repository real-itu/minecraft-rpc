# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import minecraft_pb2 as minecraft__pb2


class MinecraftServiceStub(object):
    """*
    The main service.
    """

    def __init__(self, channel):
        """Constructor.
        Args:
            channel: A grpc.Channel.
        """
        self.spawnBlocks = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/spawnBlocks',
                request_serializer=minecraft__pb2.Blocks.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.readEntities = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/readEntities',
                request_serializer=minecraft__pb2.Uuids.SerializeToString,
                response_deserializer=minecraft__pb2.Entities.FromString,
                )
        self.spawnEntities = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/spawnEntities',
                request_serializer=minecraft__pb2.SpawnEntities.SerializeToString,
                response_deserializer=minecraft__pb2.Uuids.FromString,
                )
        self.readCube = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/readCube',
                request_serializer=minecraft__pb2.Cube.SerializeToString,
                response_deserializer=minecraft__pb2.Blocks.FromString,
                )
        self.fillCube = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/fillCube',
                request_serializer=minecraft__pb2.FillCubeRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.readEntitiesInSphere = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/readEntitiesInSphere',
                request_serializer=minecraft__pb2.Sphere.SerializeToString,
                response_deserializer=minecraft__pb2.Entities.FromString,
                )
        self.executeCommands = channel.unary_unary(
                '/dk.itu.real.ooe.MinecraftService/executeCommands',
                request_serializer=minecraft__pb2.Commands.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class MinecraftServiceServicer(object):
    """*
    The main service.
    """

    def spawnBlocks(self, request, context):
        """* Spawn multiple blocks. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def readEntities(self, request, context):
        """* Reads multiple entities *
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def spawnEntities(self, request, context):
        """* Spawn multiple entities. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def readCube(self, request, context):
        """* Return all blocks in a cube 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def fillCube(self, request, context):
        """* Fill a cube with a block type 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def readEntitiesInSphere(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def executeCommands(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MinecraftServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'spawnBlocks': grpc.unary_unary_rpc_method_handler(
                    servicer.spawnBlocks,
                    request_deserializer=minecraft__pb2.Blocks.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'readEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.readEntities,
                    request_deserializer=minecraft__pb2.Uuids.FromString,
                    response_serializer=minecraft__pb2.Entities.SerializeToString,
            ),
            'spawnEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.spawnEntities,
                    request_deserializer=minecraft__pb2.SpawnEntities.FromString,
                    response_serializer=minecraft__pb2.Uuids.SerializeToString,
            ),
            'readCube': grpc.unary_unary_rpc_method_handler(
                    servicer.readCube,
                    request_deserializer=minecraft__pb2.Cube.FromString,
                    response_serializer=minecraft__pb2.Blocks.SerializeToString,
            ),
            'fillCube': grpc.unary_unary_rpc_method_handler(
                    servicer.fillCube,
                    request_deserializer=minecraft__pb2.FillCubeRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'readEntitiesInSphere': grpc.unary_unary_rpc_method_handler(
                    servicer.readEntitiesInSphere,
                    request_deserializer=minecraft__pb2.Sphere.FromString,
                    response_serializer=minecraft__pb2.Entities.SerializeToString,
            ),
            'executeCommands': grpc.unary_unary_rpc_method_handler(
                    servicer.executeCommands,
                    request_deserializer=minecraft__pb2.Commands.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dk.itu.real.ooe.MinecraftService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MinecraftService(object):
    """*
    The main service.
    """

    @staticmethod
    def spawnBlocks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/spawnBlocks',
            minecraft__pb2.Blocks.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def readEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/readEntities',
            minecraft__pb2.Uuids.SerializeToString,
            minecraft__pb2.Entities.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def spawnEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/spawnEntities',
            minecraft__pb2.SpawnEntities.SerializeToString,
            minecraft__pb2.Uuids.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def readCube(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/readCube',
            minecraft__pb2.Cube.SerializeToString,
            minecraft__pb2.Blocks.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def fillCube(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/fillCube',
            minecraft__pb2.FillCubeRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def readEntitiesInSphere(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/readEntitiesInSphere',
            minecraft__pb2.Sphere.SerializeToString,
            minecraft__pb2.Entities.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def executeCommands(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/dk.itu.real.ooe.MinecraftService/executeCommands',
            minecraft__pb2.Commands.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)