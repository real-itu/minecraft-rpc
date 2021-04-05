import grpc
from google.protobuf.any_pb2 import Any

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

uuids = client.spawnEntities(SpawnEntities(spawnEntities=[
    SpawnEntity(type=ENTITY_CREEPER, spawnPosition=Point(x=20, y=5, z=20))
]))

uuid = uuids.uuids[0]

any = Any()
any.Pack(AITASK_Idle())

#client.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=any)]))
