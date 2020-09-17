package dk.itu.real.ooe;

import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.Game;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.game.state.GamePreInitializationEvent;

import io.grpc.ServerBuilder;
import dk.itu.real.ooe.services.BlocksService;

// Imports for logger
import com.google.inject.Inject;

import java.io.IOException;

import org.slf4j.Logger;

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
    public void onPreInitialization(GamePreInitializationEvent event) throws IOException {

        // Run the block protobuf listener server

        ServerBuilder.forPort(5001).addService(new BlocksService()).build().start();
        logger.info("Listening on 5001");
    }
}
