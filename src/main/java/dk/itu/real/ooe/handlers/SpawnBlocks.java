package dk.itu.real.ooe.handlers;

import java.lang.reflect.Field;
import java.util.List;

import org.spongepowered.api.Sponge;
import org.spongepowered.api.block.BlockType;
import org.spongepowered.api.block.BlockTypes;
import org.spongepowered.api.world.World;

import dk.itu.real.ooe.BlocksOuterClass.CoordinateBlockType;
import dk.itu.real.ooe.interfaces.BlocksHandler;

public class SpawnBlocks implements BlocksHandler {

	@Override
	public String handleBlocks(List<CoordinateBlockType> blocks) {
		World world = Sponge.getServer().getWorlds().iterator().next();

		for(CoordinateBlockType block: blocks) {
			try {
				Field typeField = BlockTypes.class.getField(block.getBtype());				
				world.setBlockType(block.getX(), block.getY(), block.getZ(), (BlockType) typeField.get(null));
				
			} catch (NoSuchFieldException | SecurityException | IllegalArgumentException | IllegalAccessException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
			
		}
		return "Success?";
	}

}
