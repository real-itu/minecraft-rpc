package dk.itu_real.open_evolution.MinecraftExtendedCommands;

import java.util.List;

import foo.Test.CoordinateBlockType;
import interfaces.BlocksHandler;

public class CreateIncomingBlocks implements BlocksHandler {

	@Override
	public String handleBlocks(List<CoordinateBlockType> blocks) {
		for(CoordinateBlockType b: blocks) {
			System.out.println(b.getBtype());
			System.out.println("Success!");
		}
		return "Success!";
	}

}
