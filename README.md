# Minecraft RPC
A Python interface for Minecraft built on [gRPC](https://grpc.io)   
<br />

<p align="center">
  <img src="examples.gif">
</p>  
<br /><br />

### 1. Installing the modded Minecraft server

1. Install Java 1.8 (You can check your version with `java -version`)
   - Unix: `sudo apt-get install openjdk-8-jre`
   - OSX: 
     - `brew tap AdoptOpenJDK/openjdk`
     - `brew cask install adoptopenjdk8`
     - If troubles, check: [how to install Java on Mac OS](https://mkyong.com/java/how-to-install-java-on-mac-osx/) 
   - Install on [Windows](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html) 
2. Install grpc: `pip install grpc`
3. Create a folder `minecraft-rpc` and a subfolder `mods` inside
4. Download the latest stable [spongevanilla 1.12.2](https://www.spongepowered.org/downloads/spongevanilla/stable/1.12.2) into `minecraft-rpc` 
5. Download [minecraft-rpc jar](https://github-production-registry-package-file-4f11e5.s3.amazonaws.com/302583605/03671180-28da-11eb-8e02-5f9855a45829?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20201203%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20201203T180007Z&X-Amz-Expires=300&X-Amz-Signature=7f07216d967bb85671d1e6e473309011257c11e758aa579229841f62e9504943&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=0&response-content-disposition=filename%3Dminecraft-rpc-0.0.5.jar&response-content-type=application%2Foctet-stream) and place it in `minecraft-rpc/mods`

Your `minecraft-rpc` folder should look like (where `xxx` is the version numbers you've downloaded)
```
minecraft-rpc/
    spongevanilla-1.12.2-xxx.jar
    mods/
        minecraft-rpc-xxx.jar      
```

### 2. Starting the modded Minecraft server

1. From `minecraft-rpc`, start the server with `java -jar spongevanilla-1.12.2-xxx.jar`
2. The first time you try to start the server a texfile eula.txt with be generated, you need to modifying its last line to `eula=true` to accept the Minecraft EULA. Now running `java -jar spongevanilla-1.12.2-xxx.jar` will start the server
3. You should see a bunch of outputs including `[... INFO] [minecraft_rpc]: Listening on 5001`. 
This means it's working and the Minecraft server is ready for commands on port 5001.

### 3. Spawn blocks on the Minecraft server with Python 

Copy the files in [python client](clients/python/) to your working directory, it doesn't need to be the previously created minecraft-rpc folder. 
All you need is to have the files `minecraft_pb2.py` and `minecraft_pb2_grpc.py` on the same folder as your python script that will spawn the blocks.

There are three methods at the core of the API: `spawnBlocks` spawns a set of different blocks,
`fillCube` spawns a single type of block over a cubic volume and `readCube` which reads currently spawned blocks within a space.

Here's an [example](clients/python/example.py) on how to spawn a flying machine with python:

```python
import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
    cube=Cube(
        min=Point(x=-10, y=4, z=-10),
        max=Point(x=10, y=14, z=10)
    ),
    type=AIR
))
client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
    # Lower layer
    Block(position=Point(x=1, y=5, z=1), type=PISTON, orientation=NORTH),
    Block(position=Point(x=1, y=5, z=0), type=SLIME, orientation=NORTH),
    Block(position=Point(x=1, y=5, z=-1), type=STICKY_PISTON, orientation=SOUTH),
    Block(position=Point(x=1, y=5, z=-2), type=PISTON, orientation=NORTH),
    Block(position=Point(x=1, y=5, z=-4), type=SLIME, orientation=NORTH),
    # Upper layer
    Block(position=Point(x=1, y=6, z=0), type=REDSTONE_BLOCK, orientation=NORTH),
    Block(position=Point(x=1, y=6, z=-4), type=REDSTONE_BLOCK, orientation=NORTH),
    # Activate
    Block(position=Point(x=1, y=6, z=-1), type=QUARTZ_BLOCK, orientation=NORTH),
]))
```

To read the blocks present within a set of coordinates use `readCube`:

```python
import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

channel = grpc.insecure_channel('localhost:5001')
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

blocks = client.readCube(Cube(
         min=Point(x=0, y=0, z=0),
         max=Point(x=10, y=10, z=10)
))

print(blocks)
```



You can see the implemented Python methods at [clients/python/minecraft_pb2_grpc.py](clients/python/minecraft_pb2_grpc.py) and the general grpc definition at [src/main/proto/minecraft.proto](src/main/proto/minecraft.proto).

If you'd like to interface with the server using other languages than Python, you can use the interface definition file you can generate clients for (almost) any programming language you like. See [https://grpc.io/docs/languages/](https://grpc.io/docs/languages/)

### 3. Rendering Minecraft

You can use the method `client.readCube` that allows to read which blocks are spawned, however, if you'd like to render Minecraft to see what your spawned creations look like or even interact with them, you'll need to buy and install [Minecraft](https://www.minecraft.net)

1. Install and launch Minecraft
2. Create a compatible version:
   1. `Installations` 
   2. `New`
   3. Give it a name
   4. Select version 1.12.2 
   5. `Create`
3. Launch it:
   1. `Play`
   2. `Multiplayer`
   3. `Direct Connect`
   4. On `Server Address` write `localhost` 
   5. `Join Server`


### Et voilà:

