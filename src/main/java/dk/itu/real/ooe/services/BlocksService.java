package dk.itu.real.ooe.services;


import dk.itu.real.ooe.BlocksOuterClass;
import dk.itu.real.ooe.BlocksOuterClass.Block;
import dk.itu.real.ooe.BlocksOuterClass.Blocks;
import dk.itu.real.ooe.BlocksOuterClass.SpawnBlocksReply;
import dk.itu.real.ooe.BlocksServiceGrpc.BlocksServiceImplBase;
import io.grpc.stub.StreamObserver;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.block.BlockTypes;
import org.spongepowered.api.plugin.PluginContainer;
import org.spongepowered.api.scheduler.Task;
import org.spongepowered.api.world.World;

import java.lang.reflect.Field;
import java.util.List;

import static dk.itu.real.ooe.BlocksOuterClass.*;


public class BlocksService extends BlocksServiceImplBase {


    private final PluginContainer plugin;

    public BlocksService(PluginContainer plugin) {
        this.plugin = plugin;
    }

    @Override
    public void spawnBlocks(Blocks request, StreamObserver<SpawnBlocksReply> responseObserver) {
        Task.builder().execute(() -> {
                    List<Block> blocks = request.getBlocksList();

                    World world = Sponge.getServer().getWorlds().iterator().next();

                    for (Block block : blocks) {
                        try {
                            Field typeField = BlockTypes.class.getField(block.getType());
                            world.setBlockType(block.getX(), block.getY(), block.getZ(), (BlockType) typeField.get(null));

                        } catch (NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e) {
                            throw new RuntimeException(e);
                        }
                    }

                    responseObserver.onNext(SpawnBlocksReply.newBuilder().setStatus("ACK").build());
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
                                builder.addBlocks(Block.newBuilder()
                                        .setX(x)
                                        .setY(y).setZ(z)
                                        .setType(world.getLocation(x, y, z).getBlock().getType().getName()).build());
                            }
                        }
                    }
                    responseObserver.onNext(builder.build());
                    responseObserver.onCompleted();
                }
        ).name("readVolume").submit(plugin);
    }
}
