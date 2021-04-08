package dk.itu.real.ooe;

import com.google.inject.Inject;
import dk.itu.real.ooe.services.EntityService;
import dk.itu.real.ooe.services.MinecraftService;
import io.grpc.ServerBuilder;
import org.slf4j.Logger;
import org.spongepowered.api.Game;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.game.state.GamePreInitializationEvent;
import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.plugin.PluginContainer;

import java.io.IOException;

// Imports for logger

@Plugin(id = "minecraft_rpc", name = "Minecraft RPC", version = "1.0", description = "A plugin for Sponge which lets you control Minecraft using gRPC.")
public class MinecraftRPC {
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
        PluginContainer plugin = game.getPluginManager().getPlugin("minecraft_rpc").get();
        ServerBuilder.forPort(5001).addService(new MinecraftService(plugin)).addService(new EntityService(plugin)).build().start();
        logger.info("Listening on 5001");
    }
}
