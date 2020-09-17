package dk.itu.real.oee.services;

import java.io.IOException;
import java.util.List;

import dk.itu.real.ooe.BlocksGrpc.BlocksImplBase;
import dk.itu.real.ooe.BlocksOuterClass;
import dk.itu.real.ooe.BlocksOuterClass.CoordinateBlockType;
import dk.itu.real.ooe.interfaces.BlocksHandler;
import io.grpc.*;

public class BlocksServer extends BlocksImplBase{
	
	private BlocksHandler handler;
	
	public static void main(String[] args) throws InterruptedException {
		BlocksServer main = new BlocksServer(new BlocksHandler() {
			
			@Override
			public String handleBlocks(List<CoordinateBlockType> blocks) {
				for(CoordinateBlockType block: blocks) {
					System.out.println(block.getBtype());
				}
				return "Success?";
			}
		});
		try {
			Server server = ServerBuilder.forPort(5001).addService(main).build().start();
			server.awaitTermination();
		} catch(IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public BlocksServer(BlocksHandler blocksHandler) {
		this.handler = blocksHandler;
	}
	
	@Override
	public void setBatchBlocks(dk.itu.real.ooe.BlocksOuterClass.BatchBlockRequest request,
	        io.grpc.stub.StreamObserver<dk.itu.real.ooe.BlocksOuterClass.BatchBlockReply> responseObserver) {
		List<CoordinateBlockType> blocks = request.getBlocksList();
		
		handler.handleBlocks(blocks);
		
		responseObserver.onNext(BlocksOuterClass.BatchBlockReply.newBuilder().setStatus("ACK").build());
		responseObserver.onCompleted();
		
	}

}
