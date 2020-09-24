package dk.itu.real.ooe.services;

import dk.itu.real.ooe.BlocksOuterClass.Block;
import dk.itu.real.ooe.BlocksOuterClass.Blocks;
import dk.itu.real.ooe.BlocksOuterClass.SpawnBlocksReply;
import dk.itu.real.ooe.BlocksOuterClass.Volume;
import dk.itu.real.ooe.BlocksServiceGrpc;
import dk.itu.real.ooe.BlocksServiceGrpc.BlocksServiceBlockingStub;
import io.grpc.ManagedChannelBuilder;

import java.util.ArrayList;
import java.util.List;

import static dk.itu.real.ooe.BlocksOuterClass.BlockType.QUARTZ_BLOCK;
import static dk.itu.real.ooe.BlocksOuterClass.Orientation.UP;

public class BlocksTestClient {


    public static void main(String[] args) {
        BlocksServiceBlockingStub service = BlocksServiceGrpc.newBlockingStub(ManagedChannelBuilder.forAddress("localhost", 5001).usePlaintext().build());

        List<Block> blocks = new ArrayList<>();
        int x = -200;
        int y = 5;
        int z = 51;
        for (int i = 0; i < 100; i++) {
            blocks.add(Block.newBuilder().setX(x).setY(y).setZ(z + i).setType(QUARTZ_BLOCK).setOrientation(UP).build());
        }

        SpawnBlocksReply reply = service.spawnBlocks(Blocks.newBuilder().addAllBlocks(blocks).build());
        System.out.println(reply.getStatus());


        Blocks volume = service.readVolume(Volume.newBuilder().setX1(x).setX2(x + 1).setY1(y).setY2(y + 1).setZ1(z).setZ2(z + 10).build());
        for (Block block : volume.getBlocksList()) {
            System.out.println(block);
        }
    }
}
