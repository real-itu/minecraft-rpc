package dk.itu.real.ooe.services;


import dk.itu.real.ooe.BlocksOuterClass;
import dk.itu.real.ooe.BlocksOuterClass.*;
import dk.itu.real.ooe.BlocksServiceGrpc.BlocksServiceImplBase;
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


public class BlocksService extends BlocksServiceImplBase {


    private final PluginContainer plugin;
    private final Map<String, String> blockNamesToBlockTypes = new HashMap<>(); // minecraft:dirt --> DIRT


    public BlocksService(PluginContainer plugin) throws IllegalAccessException {
        this.plugin = plugin;

        for (Field field : BlockTypes.class.getFields()) {
            BlockType blockType = (BlockType) field.get(null);
            String key = blockType.getName();
            String value = field.getName();
            blockNamesToBlockTypes.put(key, value);
        }

    }

    @Override
    public void spawnBlocks(Blocks request, StreamObserver<SpawnBlocksReply> responseObserver) {
        Task.builder().execute(() -> {
                    List<Block> blocks = request.getBlocksList();

                    World world = Sponge.getServer().getWorlds().iterator().next();

                    for (Block block : blocks) {
                        try {
                            BlockType blockType = (BlockType) BlockTypes.class.getField(block.getType().toString()).get(null);
                            world.setBlockType(block.getX(), block.getY(), block.getZ(), blockType);
                            //TODO set orientation from block.getOrientation()
                        } catch (NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e) {
                            throw new RuntimeException(e);
                        }
                    }

                    responseObserver.onNext(SpawnBlocksReply.newBuilder().setStatus("OK").build());
                    responseObserver.onCompleted();
                }
        ).name("spawnBlocks").submit(plugin);
    }

    @Override
    public void readVolume(Volume request, StreamObserver<Blocks> responseObserver) {
        Task.builder().execute(() -> {
                    Blocks.Builder builder = Blocks.newBuilder();
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    for (int x = request.getX1(); x <= request.getX2(); x++) {
                        for (int y = request.getY1(); y <= request.getY2(); y++) {
                            for (int z = request.getZ1(); z <= request.getZ2(); z++) {
                                String name = world.getLocation(x, y, z).getBlock().getType().getName();
                                builder.addBlocks(Block.newBuilder()
                                        .setX(x)
                                        .setY(y)
                                        .setZ(z)
                                        .setType(BlocksOuterClass.BlockType.valueOf(blockNamesToBlockTypes.get(name))).build());
                            }
                        }
                    }
                    responseObserver.onNext(builder.build());
                    responseObserver.onCompleted();
                }
        ).name("readVolume").submit(plugin);
    }

    @Override
    public void fillVolume(FillVolumeRequest request, StreamObserver<FillVolumeReply> responseObserver) {
        Task.builder().execute(() -> {
                    World world = Sponge.getServer().getWorlds().iterator().next();
                    Volume v = request.getVolume();
                    for (int x = v.getX1(); x <= v.getX2(); x++) {
                        for (int y = v.getY1(); y <= v.getY2(); y++) {
                            for (int z = v.getZ1(); z <= v.getZ2(); z++) {
                                try {
                                    Field typeField = BlockTypes.class.getField(request.getType().toString());
                                    world.setBlockType(x, y, z, (BlockType) typeField.get(null));
                                } catch (NoSuchFieldException | IllegalAccessException e) {
                                    throw new RuntimeException(e);
                                }
                            }
                        }
                    }

                    responseObserver.onNext(FillVolumeReply.newBuilder().setStatus("OK").build());
                    responseObserver.onCompleted();
                }
        ).name("fillVolume").submit(plugin);
    }
}
