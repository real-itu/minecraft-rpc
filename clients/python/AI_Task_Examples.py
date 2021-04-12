import grpc
from google.protobuf.any_pb2 import Any

import minecraft_pb2_grpc
from minecraft_pb2 import *
import entities_pb2_grpc
from entities_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
entityClient = entities_pb2_grpc.EntityServiceStub(channel)

#A sheep that looks at other sheep
def watchExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=2, y=5, z=-3))
    ]))

    uuid = uuids.uuids[0]
    watch = Any()
    watch.Pack(AITask_WatchClosest(chance=100.0, maxDistance=100, entityType=ENTITY_SHEEP))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=watch)]))


#A spider that attacks sheep
def attackExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_SPIDER, spawnPosition=Point(x=2, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=4, y=5, z=-3))
    ]))

    uuid = uuids.uuids[0]
    target = Any()
    target.Pack(AITask_FindNearestTarget(chance=100, targetEntity=ENTITY_SHEEP, onlyNearby=False, shouldCheckSight=True))

    attack = Any()
    attack.Pack(AITask_AttackLiving(speed=1, hasLongMemory=True))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=target), AITask(priority=0, task=attack)]))

#A spider that only attacks one specific sheep
def attackSpecificExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_SPIDER, spawnPosition=Point(x=2, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=4, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=1, y=5, z=-3))
    ]))

    uuid = uuids.uuids[0]
    target = Any()
    target.Pack(AITask_FindSpecificTarget(chance=100, uuids=[uuids.uuids[1]], onlyNearby=False, shouldCheckSight=True))

    attack = Any()
    attack.Pack(AITask_AttackLiving(speed=1, hasLongMemory=True))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=target), AITask(priority=0, task=attack)]))


#A sheep that runs away from spiders
def avoidTypesExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_SPIDER, spawnPosition=Point(x=2, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=4, y=5, z=-3))
    ]))

    uuid = uuids.uuids[1]
    run = Any()
    run.Pack(AITask_AvoidEntityTypes(closeRangeSpeed=5.0, farRangeSpeed=5.0, searchDistance=200.0, entityType=[ENTITY_SPIDER]))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=run)]))

#A sheep that only runs away from a specific spider
def avoidSpecificsExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_SPIDER, spawnPosition=Point(x=2, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=4, y=5, z=-3))
    ]))

    uuid = uuids.uuids[1]
    run = Any()
    run.Pack(AITask_AvoidSpecificEntities(closeRangeSpeed=5.0, farRangeSpeed=5.0, searchDistance=200.0, uuids=[uuids.uuids[0]]))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=run)]))


#A witch that shoots sheep
def rangedAttackExample():
    uuids = entityClient.spawnEntities(SpawnEntities(spawnEntities=[
        SpawnEntity(type=ENTITY_WITCH, spawnPosition=Point(x=2, y=5, z=-3)),
        SpawnEntity(type=ENTITY_SHEEP, spawnPosition=Point(x=4, y=5, z=-3))
    ]))

    uuid = uuids.uuids[0]
    target = Any()
    target.Pack(AITask_FindNearestTarget(chance=100, targetEntity=ENTITY_SHEEP, onlyNearby=False, shouldCheckSight=True))

    rangeAttack = Any()
    rangeAttack.Pack(AITask_RangeAgent(attackRadius=100.0, delayBetweenAttacks=1, moveSpeed=1.0))

    entityClient.updateEntityAI(EntityAIUpdate(uuid=uuid, resetGoals=True, AITasks=[AITask(priority=0,task=target), AITask(priority=0, task=rangeAttack)]))
