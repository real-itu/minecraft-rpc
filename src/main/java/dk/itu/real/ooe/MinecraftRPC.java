package dk.itu.real.ooe;

import com.google.inject.Inject;
import dk.itu.real.ooe.services.MinecraftService;
import io.grpc.ServerBuilder;
import org.slf4j.Logger;
import org.spongepowered.api.Game;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.game.state.GamePreInitializationEvent;
import org.spongepowered.api.plugin.Plugin;
import org.spongepowered.api.plugin.PluginContainer;

import java.io.IOException;

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
        ForceChunkLoadListener chunkLoader = new ForceChunkLoadListener();
        MinecraftService service = new MinecraftService(plugin, chunkLoader);
        Sponge.getEventManager().registerListeners(this, chunkLoader);
        ServerBuilder.forPort(5002).addService(service).build().start();
        logger.info("Listening on 5002");
    }
}
