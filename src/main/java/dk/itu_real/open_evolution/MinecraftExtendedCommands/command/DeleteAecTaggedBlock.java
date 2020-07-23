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

public class DeleteAecTaggedBlock implements CommandExecutor {
	
    // private MinecraftExtendedCommands plugin;
    private Logger logger;
    Map<Text, Entity> entity_dict;

    public DeleteAecTaggedBlock(Logger logger, Map<Text, Entity> entity_dict) {
        this.logger = logger;
        this.entity_dict = entity_dict;
    }

    @Override
    public CommandResult execute(CommandSource src, CommandContext args) throws CommandException {
        String tag = (String) args.getOne("entity_tag").orElse(null);
        
        if(!entity_dict.containsKey(Text.of(tag))) {
        	src.sendMessage(Text.of("Tag doesn't exist"));
        	src.sendMessage(Text.of("Operation unsuccesful!"));
        	return CommandResult.affectedBlocks(0);
        }

        logger.debug("Received tag " + tag);
        
        Entity aec = entity_dict.get(Text.of(tag));
        entity_dict.remove(Text.of(tag));
        aec.remove();
        src.sendMessage(Text.of("AEC tag removes"));
        
        return CommandResult.success();
    }

}
