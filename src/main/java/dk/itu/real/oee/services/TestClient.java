package dk.itu.real.oee.services;

import java.lang.reflect.Field;
import java.util.ArrayList;

import org.spongepowered.api.block.BlockTypes;

import dk.itu.real.ooe.BlocksGrpc;
import dk.itu.real.ooe.BlocksGrpc.BlocksBlockingStub;
import dk.itu.real.ooe.BlocksOuterClass.BatchBlockReply;
import dk.itu.real.ooe.BlocksOuterClass.BatchBlockRequest;
import dk.itu.real.ooe.BlocksOuterClass.CoordinateBlockType;
import io.grpc.ManagedChannelBuilder;

public class TestClient {
	
	
	public static CoordinateBlockType getCoordinateBlockType(String blockType, int x, int y, int z) {
		return CoordinateBlockType.newBuilder().setX(x).setY(y).setZ(z).setBtype(blockType).build();
	}
	public static void main(String[] args) {
		BlocksBlockingStub bs = BlocksGrpc.newBlockingStub(ManagedChannelBuilder.forAddress("localhost", 5001).usePlaintext().build());
		
		ArrayList<CoordinateBlockType> blocks = new ArrayList<CoordinateBlockType>();
		int start_x  = -200;
		int start_y = 5;
		int start_z = 51;
		blocks.add(getCoordinateBlockType("SLIME", start_x, start_y, start_z));
		blocks.add(getCoordinateBlockType("QUARTZ_BLOCK", start_x, start_y, start_z+1));
		
		BatchBlockRequest request = BatchBlockRequest.newBuilder().addAllBlocks(blocks).build();
		
		BatchBlockReply reply = bs.setBatchBlocks(request);
		System.out.println(reply.getStatus());

		
	}
}
