package dk.itu.real.ooe;

import com.flowpowered.math.vector.Vector3i;
import org.spongepowered.api.Sponge;
import org.spongepowered.api.entity.Entity;
import org.spongepowered.api.event.Listener;
import org.spongepowered.api.event.world.chunk.LoadChunkEvent;
import org.spongepowered.api.world.World;

import java.util.*;

public class ForceChunkLoadListener {

    private Map<Vector3i, List<Entity>> entityQueue = new HashMap<>();

    public void addToEntityQueue(Entity entity){
        Vector3i chunkPosition = entity.getLocation().getChunkPosition();
        if(entityQueue.containsKey(chunkPosition)){
            entityQueue.get(chunkPosition).add(entity);
        } else {
            entityQueue.put(chunkPosition, new ArrayList<>(Collections.singletonList(entity)));
        }
    }

    @Listener
    public void onForceChunkLoad(LoadChunkEvent event){
        World world = Sponge.getServer().getWorlds().iterator().next();
        if(entityQueue.containsKey(event.getTargetChunk().getPosition())){
            world.spawnEntities(entityQueue.get(event.getTargetChunk().getPosition()));
        }
    }
}
