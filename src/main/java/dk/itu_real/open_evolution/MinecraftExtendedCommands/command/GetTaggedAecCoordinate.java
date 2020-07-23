package dk.itu_real.open_evolution.MinecraftExtendedCommands.command;

import java.util.Map;

import org.slf4j.Logger;
import org.spongepowered.api.command.CommandException;
import org.spongepowered.api.command.CommandResult;
import org.spongepowered.api.command.CommandSource;
import org.spongepowered.api.command.args.CommandContext;
import org.spongepowered.api.command.spec.CommandExecutor;
import org.spongepowered.api.entity.Entity;
import org.spongepowered.api.text.Text;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;

public class GetTaggedAecCoordinate implements CommandExecutor {
	
    // private MinecraftExtendedCommands plugin;
    private Logger logger;
    Map<Text, Entity> entity_dict;

    public GetTaggedAecCoordinate(Logger logger, Map<Text, Entity> entity_dict) {
        this.logger = logger;
        this.entity_dict = entity_dict;
    }

    @Override
    public CommandResult execute(CommandSource src, CommandContext args) throws CommandException {
        String aec_tag = (String) args.getOne("entity_tag").orElse(null);
        
        if(!entity_dict.containsKey(Text.of(aec_tag))) {
        	src.sendMessage(Text.of("Tag doesn't exist"));
        	return CommandResult.affectedBlocks(0);
        }
        
        logger.debug("Received tag " + aec_tag);
        Entity aec = this.entity_dict.get(Text.of(aec_tag));
        Location<World> aec_location = aec.getLocation();
        src.sendMessage(Text.of(aec_location.toString()));
        
        return CommandResult.success();
    }

}