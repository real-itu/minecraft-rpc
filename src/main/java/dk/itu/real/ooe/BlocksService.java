package dk.itu.real.ooe;

import io.grpc.stub.StreamObserver;


public class BlocksService extends BlocksGrpc.BlocksImplBase {

    @Override
    public void setBatchBlocks(BlocksOuterClass.BatchBlockRequest request, StreamObserver<BlocksOuterClass.BatchBlockReply> responseObserver) {
        throw new UnsupportedOperationException(); //TODO @djordje
    }
}
