package dk.itu.real.ooe;

import com.google.inject.Inject;
import dk.itu.real.ooe.services.BlocksService;
import io.grpc.ServerBuilder;
import org.slf4j.Logger;
import org.spongepowered.api.Game;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.game.state.GamePreInitializationEvent;
import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.plugin.PluginContainer;

import java.io.IOException;

// Imports for logger

@Plugin(id = "minecraft_extended_commands", name = "Minecraft Extended Commands", version = "1.0", description = "Adding extra commands to help Python")
public class MinecraftExtendedCommands {
    @Inject
    private Game game;
    @Inject
    private Logger logger;

    /**
     * Called on server startup.
     *
     * @param event The server startup event
     */
    @Listener
    public void onPreInitialization(GamePreInitializationEvent event) throws IOException, IllegalAccessException {
        PluginContainer plugin = game.getPluginManager().getPlugin("minecraft_extended_commands").get();
        ServerBuilder.forPort(5001).addService(new BlocksService(plugin)).build().start();
        logger.info("Listening on 5001");
    }
}
