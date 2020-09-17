package dk.itu.real.ooe.services;

import dk.itu.real.ooe.BlocksOuterClass.*;
import dk.itu.real.ooe.BlocksServiceGrpc;
import dk.itu.real.ooe.BlocksServiceGrpc.*;
import io.grpc.ManagedChannelBuilder;

import java.util.ArrayList;
import java.util.List;

public class BlocksTestClient {


    public static Block getCoordinateBlockType(String blockType, int x, int y, int z) {
        return Block.newBuilder().setX(x).setY(y).setZ(z).setType(blockType).build();
    }

    public static void main(String[] args) {
        BlocksServiceBlockingStub service = BlocksServiceGrpc.newBlockingStub(ManagedChannelBuilder.forAddress("localhost", 5001).usePlaintext().build());

        List<Block> blocks = new ArrayList<>();
        int start_x = -200;
        int start_y = 5;
        int start_z = 51;
        blocks.add(getCoordinateBlockType("SLIME", start_x, start_y, start_z));
        blocks.add(getCoordinateBlockType("QUARTZ_BLOCK", start_x, start_y, start_z + 1));

        SpawnBlocksReply reply = service.spawnBlocks(Blocks.newBuilder().addAllBlocks(blocks).build());
        System.out.println(reply.getStatus());
    }
}
