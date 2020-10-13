package dk.itu.real.ooe.services;


import com.google.protobuf.Empty;
import dk.itu.real.ooe.Minecraft;
import dk.itu.real.ooe.Minecraft.*;
import dk.itu.real.ooe.MinecraftServiceGrpc.MinecraftServiceImplBase;
import io.grpc.stub.StreamObserver;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.block.BlockTypes;
import org.spongepowered.api.plugin.PluginContainer;
import org.spongepowered.api.scheduler.Task;
import org.spongepowered.api.world.World;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


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
                            world.setBlockType(pos.getX(), pos.getY(), pos.getZ(), blockType);
                            //TODO set orientation from block.getOrientation()
                        } catch (NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e) {
                            throw new RuntimeException(e);
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
}
