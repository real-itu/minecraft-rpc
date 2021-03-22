package dk.itu.real.ooe;

import org.spongepowered.api.Sponge;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.world.chunk.ForcedChunkEvent;
import org.spongepowered.api.world.World;

public class ForceChunkLoadListener {
    @Listener
    public void onForceChunkLoad(ForcedChunkEvent event){
        World world = Sponge.getServer().getWorlds().iterator().next();
        //world.spawnEntities(entityQueue.get(event.getChunkCoords()));
    }
}
