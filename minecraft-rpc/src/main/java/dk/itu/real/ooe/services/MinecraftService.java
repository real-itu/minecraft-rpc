package dk.itu.real.ooe.services;

import com.google.protobuf.Empty;
import dk.itu.real.ooe.Minecraft;
import dk.itu.real.ooe.Minecraft.*;
import dk.itu.real.ooe.MinecraftServiceGrpc.MinecraftServiceImplBase;
import io.grpc.stub.StreamObserver;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.entity.Entity;
import org.spongepowered.api.entity.EntityTypes;
import org.spongepowered.api.event.cause.EventContextKeys;
import org.spongepowered.api.event.CauseStackManager.StackFrame;
import org.spongepowered.api.event.cause.entity.spawn.SpawnTypes;
import org.spongepowered.api.block.BlockState;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.block.BlockTypes;
import org.spongepowered.api.data.key.Keys;
import org.spongepowered.api.data.manipulator.mutable.block.DirectionalData;
import org.spongepowered.api.plugin.PluginContainer;
import org.spongepowered.api.scheduler.Task;
import org.spongepowered.api.util.Direction;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;
import org.spongepowered.api.command.CommandManager;
import com.flowpowered.math.vector.Vector3d;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.ArrayList;


public class MinecraftService extends MinecraftServiceImplBase {


    private final PluginContainer plugin;
    private final Map<String, String> blockNamesToBlockTypes = new HashMap<>(); // minecraft:dirt --> DIRT
    private final Map<String, String> entityNamesToEntityTypes = new HashMap<>(); //minecraft:creeper --> CREEPER


    public MinecraftService(PluginContainer plugin) throws IllegalAccessException {
        this.plugin = plugin;

        for (Field field : BlockTypes.class.getFields()) {
            BlockType blockType = (BlockType) field.get(null);
            String key = blockType.getName();
            String value = field.getName();
            blockNamesToBlockTypes.put(key, value);
        }

        for (Field field : EntityTypes.class.getFields()) {
            org.spongepowered.api.entity.EntityType entityType = (org.spongepowered.api.entity.EntityType) field.get(null);
            String key = entityType.getName();
            String value = field.getName();
            entityNamesToEntityTypes.put(key, value);
        }
    }

    @Override
    public void spawnBlocks(Blocks request, StreamObserver<Empty> responseObserver) {
        Task.builder().execute(() -> {
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    for (Block block : request.getBlocksList()) {
                        try {
                            BlockType blockType = (BlockType) BlockTypes.class.getField(block.getType().toString()).get(null);
                            Point pos = block.getPosition();
                            Orientation orientation = block.getOrientation();
                            world.setBlockType(pos.getX(), pos.getY(), pos.getZ(), blockType);
                            if (blockType.getDefaultState().supports(Keys.DIRECTION)) {
                                setOrientation(world.getLocation(pos.getX(), pos.getY(), pos.getZ()), orientation, blockType);
                            }
                        } catch (IllegalStateException | NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e ){
                            this.plugin.getLogger().info(e.getMessage());
                        }
                    }

                    responseObserver.onNext(Empty.getDefaultInstance());
                    responseObserver.onCompleted();
                }
        ).name("spawnBlocks").submit(plugin);
    }

    @Override
    public void readEntitiesInSphere(Sphere request, StreamObserver<Entities> responseObserver) {
        Task.builder().execute(() -> {
                Entities.Builder builder = Entities.newBuilder();
                World world = Sponge.getServer().getWorlds().iterator().next();
                ArrayList<Entity> entities = (ArrayList<Entity>) world.getNearbyEntities(new Vector3d(request.getCenter().getX(), request.getCenter().getY(), request.getCenter().getZ()), request.getRadius());
                for (Entity entity : entities) {
	                builder.addEntities(Minecraft.Entity.newBuilder()
                            .setId(entity.getUniqueId().toString())
                            .setType(Minecraft.EntityType.valueOf("ENTITY_" + entityNamesToEntityTypes.get(entity.getType().getName())))
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
                    builder.addEntities(Minecraft.Entity.newBuilder()
                        //Proto ignores defualt values so there is no need to set type, position and isloaded
                        .setId(id)).build();
                } else {
                    org.spongepowered.api.entity.Entity entity = entityOption.get();
                    Location location = entity.getLocation();
                    builder.addEntities(Minecraft.Entity.newBuilder()
                        .setId(id)
                        .setType(Minecraft.EntityType.valueOf("ENTITY_" + entityNamesToEntityTypes.get(entity.getType().getName())))
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
            for (dk.itu.real.ooe.Minecraft.SpawnEntity entity : request.getSpawnEntitiesList()) {
                try {
                    org.spongepowered.api.entity.EntityType entityType = (org.spongepowered.api.entity.EntityType) EntityTypes.class.getField(entity.getType().toString().split("_", 2)[1]).get(null);
                    Point pos = entity.getSpawnPosition();
                    org.spongepowered.api.entity.Entity newEntity = world.createEntity(entityType, new Vector3d(pos.getX(), pos.getY(), pos.getZ()));
                    try (StackFrame frame = Sponge.getCauseStackManager().pushCauseFrame()) {
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
    public void readCube(Cube cube, StreamObserver<Blocks> responseObserver) {
        Task.builder().execute(() -> {
                    Blocks.Builder builder = Blocks.newBuilder();
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    Point min = cube.getMin();
                    Point max = cube.getMax();
                    for (int x = min.getX(); x <= max.getX(); x++) {
                        for (int y = min.getY(); y <= max.getY(); y++) {
                            for (int z = min.getZ(); z <= max.getZ(); z++) {
                                String name = world.getLocation(x, y, z).getBlock().getType().getName();
                                builder.addBlocks(Block.newBuilder()
                                        .setPosition(Point.newBuilder()
                                                .setX(x)
                                                .setY(y)
                                                .setZ(z)
                                                .build()
                                        )
                                        .setType(Minecraft.BlockType.valueOf(blockNamesToBlockTypes.get(name))).build());
                            }
                        }
                    }
                    responseObserver.onNext(builder.build());
                    responseObserver.onCompleted();
                }
        ).name("readCube").submit(plugin);
    }

    @Override
    public void fillCube(FillCubeRequest request, StreamObserver<Empty> responseObserver) {
        Task.builder().execute(() -> {
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    Cube c = request.getCube();
                    Point min = c.getMin();
                    Point max = c.getMax();
                    BlockType type;
                    try {
                        Field typeField = BlockTypes.class.getField(request.getType().toString());
                        type = (BlockType) typeField.get(null);
                    } catch (NoSuchFieldException | IllegalAccessException e) {
                        throw new RuntimeException(e);
                    }

                    for (int x = min.getX(); x <= max.getX(); x++) {
                        for (int y = min.getY(); y <= max.getY(); y++) {
                            for (int z = min.getZ(); z <= max.getZ(); z++) {
                                world.setBlockType(x, y, z, type);
                            }
                        }
                    }

                    responseObserver.onNext(Empty.getDefaultInstance());
                    responseObserver.onCompleted();
                }
        ).name("fillCube").submit(plugin);
    }

    @Override
    public void executeCommands(Commands commands, StreamObserver<Empty> responseObserver){
        CommandManager cmdManager = Sponge.getCommandManager();
        for(Command command : commands.getCommandsList()){
            cmdManager.process(Sponge.getServer().getConsole(), command.getCommand());
        }
        responseObserver.onNext(Empty.getDefaultInstance());
        responseObserver.onCompleted();
    }


    public void setOrientation(Location<World> blockLoc, Orientation orientation, BlockType btype) throws IllegalStateException{
        Optional<DirectionalData> optionalData = blockLoc.get(DirectionalData.class);
        if (!optionalData.isPresent()) {
            throw new IllegalStateException("Failed to get block location data");
        }
        DirectionalData data = optionalData.get();
        data.set(Keys.DIRECTION, Direction.valueOf(orientation.toString()));
        BlockState state = btype.getDefaultState();
        Optional<BlockState> newState = state.with(data.asImmutable());
        if (!newState.isPresent()) {
            throw new IllegalStateException("block type " + btype.toString() + " failed to set orientation!");
        }
        blockLoc.setBlock(newState.get());
    }

}
