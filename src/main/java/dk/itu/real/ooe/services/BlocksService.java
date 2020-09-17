package dk.itu.real.ooe.services;


import dk.itu.real.ooe.BlocksOuterClass.*;
import dk.itu.real.ooe.BlocksServiceGrpc.*;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.block.BlockTypes;
import org.spongepowered.api.world.World;

import java.io.IOException;
import java.lang.reflect.Field;
import java.util.List;


public class BlocksService extends BlocksServiceImplBase {

    public static void main(String[] args) throws InterruptedException, IOException {
        BlocksService blocksService = new BlocksService();
        Server server = ServerBuilder.forPort(5001).addService(blocksService).build().start();
        server.awaitTermination();
    }

    @Override
    public void spawnBlocks(Blocks request, StreamObserver<SpawnBlocksReply> responseObserver) {
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


}
