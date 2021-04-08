package dk.itu.real.ooe.services;

import com.flowpowered.math.vector.Vector3d;
import com.google.protobuf.Empty;
import com.google.protobuf.InvalidProtocolBufferException;
import dk.itu.real.ooe.EntitiesOuterClass.*;
import dk.itu.real.ooe.EntityServiceGrpc.EntityServiceImplBase;
import dk.itu.real.ooe.SharedMessages.*;

import org.spongepowered.api.Sponge;
import org.spongepowered.api.entity.EntityTypes;
import org.spongepowered.api.entity.ai.Goal;
import org.spongepowered.api.entity.ai.GoalTypes;
import org.spongepowered.api.entity.ai.task.builtin.LookIdleAITask;
import org.spongepowered.api.entity.ai.task.builtin.WatchClosestAITask;
import org.spongepowered.api.entity.ai.task.builtin.creature.AttackLivingAITask;
import org.spongepowered.api.entity.living.Agent;
import org.spongepowered.api.entity.living.Creature;
import org.spongepowered.api.event.CauseStackManager;
import org.spongepowered.api.event.cause.EventContextKeys;
import org.spongepowered.api.event.cause.entity.spawn.SpawnTypes;
import org.spongepowered.api.plugin.PluginContainer;
import org.spongepowered.api.entity.Entity;

import io.grpc.stub.StreamObserver;
import org.spongepowered.api.scheduler.Task;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;

import java.lang.reflect.Field;
import java.util.*;

public class EntityService extends EntityServiceImplBase {

    private final PluginContainer plugin;
    private final Map<String, String> entityNamesToEntityTypes = new HashMap<>(); //minecraft:creeper --> CREEPER

    public EntityService(PluginContainer plugin) throws IllegalAccessException {
        this.plugin = plugin;

        for (Field field : EntityTypes.class.getFields()) {
            org.spongepowered.api.entity.EntityType entityType = (org.spongepowered.api.entity.EntityType) field.get(null);
            String key = entityType.getName();
            String value = field.getName();
            entityNamesToEntityTypes.put(key, value);
        }
    }

    @Override
    public void readEntitiesInSphere(Sphere request, StreamObserver<Entities> responseObserver){
        Task.builder().execute(() -> {
                    Entities.Builder builder = Entities.newBuilder();
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    ArrayList<Entity> entities = (ArrayList<Entity>) world.getNearbyEntities(new Vector3d(request.getCenter().getX(), request.getCenter().getY(), request.getCenter().getZ()), request.getRadius());
                    for (Entity entity : entities) {
                        builder.addEntities(dk.itu.real.ooe.EntitiesOuterClass.Entity.newBuilder()
                                .setId(entity.getUniqueId().toString())
                                .setType(EntityType.valueOf("ENTITY_" + entityNamesToEntityTypes.get(entity.getType().getName())))
                                .setPosition(Point.newBuilder()
                                        .setX((int)entity.getLocation().getX())
                                        .setY((int)entity.getLocation().getY())
                                        .setZ((int)entity.getLocation().getZ())
                                        .build())
                                .setIsLoaded(entity.isLoaded()))
                                .build();
                    }
                    responseObserver.onNext(builder.build());
                    responseObserver.onCompleted();
                }
        ).name("readCube").submit(plugin);
    }

    @Override
    public void readEntities(Uuids request, StreamObserver<Entities> responseObserver) {
        Task.builder().execute(() -> {
            Entities.Builder builder = Entities.newBuilder();
            World world = Sponge.getServer().getWorlds().iterator().next();
            for(String id : request.getUuidsList()) {
                Optional<Entity> entityOption = world.getEntity(UUID.fromString(id));
                if(!entityOption.isPresent()){
                    builder.addEntities(dk.itu.real.ooe.EntitiesOuterClass.Entity.newBuilder()
                            //Proto ignores defualt values so there is no need to set type, position and isloaded
                            .setId(id)).build();
                } else {
                    org.spongepowered.api.entity.Entity entity = entityOption.get();
                    Location location = entity.getLocation();
                    builder.addEntities(dk.itu.real.ooe.EntitiesOuterClass.Entity.newBuilder()
                            .setId(id)
                            .setType(dk.itu.real.ooe.EntitiesOuterClass.EntityType.valueOf("ENTITY_" + entityNamesToEntityTypes.get(entity.getType().getName())))
                            .setPosition(Point.newBuilder()
                                    .setX((int)location.getX())
                                    .setY((int)location.getY())
                                    .setZ((int)location.getZ())
                                    .build())
                            .setIsLoaded(entity.isLoaded())
                    ).build();
                }
            }
            responseObserver.onNext(builder.build());
            responseObserver.onCompleted();
        }).name("spawnEntities").submit(plugin);
    }

    @Override
    public void spawnEntities(SpawnEntities request, StreamObserver<Uuids> responseObserver){
        Task.builder().execute(() -> {
            Uuids.Builder builder = Uuids.newBuilder();
            World world = Sponge.getServer().getWorlds().iterator().next();
            for (SpawnEntity entity : request.getSpawnEntitiesList()) {
                try {
                    org.spongepowered.api.entity.EntityType entityType = (org.spongepowered.api.entity.EntityType) EntityTypes.class.getField(entity.getType().toString().split("_", 2)[1]).get(null);
                    Point pos = entity.getSpawnPosition();
                    org.spongepowered.api.entity.Entity newEntity = world.createEntity(entityType, new Vector3d(pos.getX(), pos.getY(), pos.getZ()));
                    try (CauseStackManager.StackFrame frame = Sponge.getCauseStackManager().pushCauseFrame()) {
                        frame.addContext(EventContextKeys.SPAWN_TYPE, SpawnTypes.PLUGIN);
                        world.spawnEntity(newEntity);
                    }
                    builder.addUuids(newEntity.getUniqueId().toString()).build();
                } catch (IllegalStateException | NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e){
                    this.plugin.getLogger().info(e.getMessage());
                }
            }
            responseObserver.onNext(builder.build());
            responseObserver.onCompleted();
        }).name("spawnEntities").submit(plugin);
    }

    @Override
    public void updateEntityAI(EntityAIUpdate request, StreamObserver<Empty> responseObserver){
        Task.builder().execute(() -> {
            World world = Sponge.getServer().getWorlds().iterator().next();
            Agent agent = (Agent) world.getEntity(UUID.fromString(request.getUuid())).get();
            if(request.getResetGoals()){
                //Clear goals if they exist
                Optional<Goal<Agent>> normalGoal = agent.getGoal(GoalTypes.NORMAL);
                normalGoal.ifPresent(Goal::clear);
                Optional<Goal<Agent>> targetGoal = agent.getGoal(GoalTypes.TARGET);
                targetGoal.ifPresent(Goal::clear);
            }
            try {
                configureAITasks(agent, request.getAITasksList());
            } catch (InvalidProtocolBufferException | NoSuchFieldException | IllegalAccessException e) {
                //TODO: handle this
                e.printStackTrace();
            }
            responseObserver.onNext(Empty.getDefaultInstance());
            responseObserver.onCompleted();
        }).name("updateEntityAI").submit(plugin);
    }

    private void configureAITasks(Agent agent, List<AITask> tasks) throws InvalidProtocolBufferException, NoSuchFieldException, IllegalAccessException {
        Goal<Agent> goal = agent.getGoal(GoalTypes.NORMAL).get();
        for (AITask task: tasks) {
            if(task.getTask().is(AITask_Idle.class)){
                LookIdleAITask idle = LookIdleAITask.builder().build(agent);
                goal.addTask(task.getPriority(), idle);
                System.out.println("hello from idle");
            }else if(task.getTask().is(AITask_WatchClosest.class)){
                AITask_WatchClosest watchClosest = task.getTask().unpack(AITask_WatchClosest.class);
                //TODO: Fix this monstrosity
                org.spongepowered.api.entity.EntityType type = (org.spongepowered.api.entity.EntityType) EntityTypes.class.getField(agent.getType().toString().split("_", 2)[1]).get(null);
                WatchClosestAITask newTask = WatchClosestAITask.builder()
                        .chance(watchClosest.getChance())
                        .maxDistance(watchClosest.getMaxDistance())
                        .watch(type.getEntityClass())
                        .build(agent);
                goal.addTask(task.getPriority(), newTask);
            } else if(task.getTask().is(AITask_AttackLiving.class)){
                AITask_AttackLiving attackLiving = task.getTask().unpack(AITask_AttackLiving.class);
                AttackLivingAITask.Builder newTaskBuilder = AttackLivingAITask.builder()
                        .speed(attackLiving.getSpeed());
                if(attackLiving.getHasLongMemory()){
                    newTaskBuilder.longMemory();
                }
                AttackLivingAITask newTask = newTaskBuilder.build((Creature) agent);
                goal.addTask(task.getPriority(), newTask);
            } else {
                throw new RuntimeException("AI Task not recognised");
            }
        }
    }
}
