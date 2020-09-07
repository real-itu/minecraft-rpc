package dk.itu_real.open_evolution.MinecraftExtendedCommands.command;

import java.util.Map;

import org.slf4j.Logger;
import org.spongepowered.api.command.CommandException;
import org.spongepowered.api.command.CommandResult;
import org.spongepowered.api.command.CommandSource;
import org.spongepowered.api.command.args.CommandContext;
import org.spongepowered.api.command.spec.CommandExecutor;
import org.spongepowered.api.entity.Entity;
import org.spongepowered.api.entity.EntityTypes;
import org.spongepowered.api.text.Text;
import org.spongepowered.api.world.Location;
import org.spongepowered.api.world.World;

import org.spongepowered.api.data.manipulator.mutable.entity.AreaEffectCloudData;
import org.spongepowered.api.data.value.mutable.MutableBoundedValue;

import java.util.UUID;

public class AddAecAtCoordinate implements CommandExecutor {
	
    // private MinecraftExtendedCommands plugin;
    private Logger logger;
    Map<Text, UUID> entity_dict;

    public AddAecAtCoordinate(Logger logger, Map<Text, UUID> entity_dict) {
        this.logger = logger;
        this.entity_dict = entity_dict;
    }

    @Override
    public CommandResult execute(CommandSource src, CommandContext args) throws CommandException {
        @SuppressWarnings("unchecked")
		Location<World> location = (Location<World>) args.getOne("location").orElse(null);
        String tag = (String) args.getOne("entity_tag").orElse(null);

        if(entity_dict.containsKey(Text.of(tag))) {
        	src.sendMessage(Text.of("Tag already exists"));
        	return CommandResult.affectedBlocks(0);
        }
        
        logger.debug("Received location " + location.toString());
        World world = location.getExtent();
        
        Entity aec = world.createEntity(EntityTypes.AREA_EFFECT_CLOUD, location.getPosition());
        
        // AreaEffectCloudData aec_data = aec.get(AreaEffectCloudData.class).get();
        // aec_data.duration().set(aec_data.duration().getMaxValue());
        // aec.offer(aec_data.duration().set(aec_data.duration().getMaxValue()));
        
        world.spawnEntity(aec);
        UUID aec_uuid = aec.getUniqueId();
        entity_dict.put(Text.of(tag), aec_uuid);
        
        src.sendMessage(Text.of(aec_uuid.toString()));
        return CommandResult.success();
    }

}
