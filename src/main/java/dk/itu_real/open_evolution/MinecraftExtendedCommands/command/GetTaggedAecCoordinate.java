package dk.itu_real.open_evolution.MinecraftExtendedCommands.command;

import java.util.Map;
import java.util.Optional;

import org.slf4j.Logger;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.command.CommandException;
import org.spongepowered.api.command.CommandResult;
import org.spongepowered.api.command.CommandSource;
import org.spongepowered.api.command.args.CommandContext;
import org.spongepowered.api.command.spec.CommandExecutor;
import org.spongepowered.api.entity.Entity;
import org.spongepowered.api.text.Text;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;
import java.util.UUID;

public class GetTaggedAecCoordinate implements CommandExecutor {
	
    // private MinecraftExtendedCommands plugin;
    private Logger logger;
    Map<Text, UUID> entity_dict;

    public GetTaggedAecCoordinate(Logger logger, Map<Text, UUID> entity_dict) {
        this.logger = logger;
        this.entity_dict = entity_dict;
    }
    
    private void sendEntityLocation(Entity entity, CommandSource src) {
    	Location<World> entity_location = entity.getLocation();
        src.sendMessage(Text.of(entity_location.toString()));
    }

    @Override
    public CommandResult execute(CommandSource src, CommandContext args) throws CommandException {
        String aec_tag = (String) args.getOne("entity_tag").orElse(null);
        World world = Sponge.getServer().getWorlds().iterator().next();
        
        if(!entity_dict.containsKey(Text.of(aec_tag))) {
        	src.sendMessage(Text.of("Tag doesn't exist"));
        	return CommandResult.affectedBlocks(0);
        }
        
        logger.debug("Received tag " + aec_tag);
        UUID aec_uuid = this.entity_dict.get(Text.of(aec_tag));
        Optional<Entity> optional_aec = world.getEntity(aec_uuid);
        if(optional_aec.isPresent()){
        	this.sendEntityLocation(optional_aec.get(), src);
        	return CommandResult.success();
        } else {
        	src.sendMessage(Text.of("ERROR: Entity doesn't exist anymore"));
        	this.entity_dict.remove(Text.of(aec_tag));
        	return CommandResult.affectedBlocks(0);
        }
    }

}