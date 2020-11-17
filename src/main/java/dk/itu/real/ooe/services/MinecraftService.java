package dk.itu.real.ooe.services;


import com.google.protobuf.Empty;
import dk.itu.real.ooe.Minecraft;
import dk.itu.real.ooe.Minecraft.*;
import dk.itu.real.ooe.MinecraftServiceGrpc.MinecraftServiceImplBase;
import io.grpc.stub.StreamObserver;
import org.spongepowered.api.Sponge;
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

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;


public class MinecraftService extends MinecraftServiceImplBase {


    private final PluginContainer plugin;
    private final Map<String, String> blockNamesToBlockTypes = new HashMap<>(); // minecraft:dirt --> DIRT


    public MinecraftService(PluginContainer plugin) throws IllegalAccessException {
        this.plugin = plugin;

        for (Field field : BlockTypes.class.getFields()) {
            BlockType blockType = (BlockType) field.get(null);
            String key = blockType.getName();
            String value = field.getName();
            blockNamesToBlockTypes.put(key, value);
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
                            try {
                                if (blockType.getDefaultState().supports(Keys.DIRECTION)) {
                                    setOrientation(world.getLocation(pos.getX(), pos.getY(), pos.getZ()), orientation, blockType);
                                }
                            }catch (IllegalStateException e){
                                System.err.println(e.getMessage());
                            }
                        } catch (IllegalStateException | NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e ) {
                            System.err.println(e.getMessage());
                        }
                    }

                    responseObserver.onNext(Empty.getDefaultInstance());
                    responseObserver.onCompleted();
                }
        ).name("spawnBlocks").submit(plugin);
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
