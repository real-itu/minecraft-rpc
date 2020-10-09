# Minecraft RPC
A [gRPC](https://grpc.io) interface for Minecraft

### Starting the modded Minecraft server

* Install Java 1.8 (You can check your version with `java -version`)
* Create a folder `minecraft-rpc`
* Download the latest stable [spongevanilla 1.12.2](https://www.spongepowered.org/downloads/spongevanilla/stable/1.12.2) into `minecraft-rpc` 
* Download the latest [minecraft-rpc jar](https://github.com/real-itu/minecraft-rpc/packages/434436) into `minecraft-rpc/mods`
* Your `minecraft-rpc` should look like (where `xxx` are version numbers)
```
minecraft-rpc/
    spongevanilla-1.12.2-xxx.jar
    mods/
        minecraft-rpc-xxx.jar      
```
* Start the server with `java -jar spongevanilla-1.12.2-xxx.jar`
* The first time you start the server you must accept the Minecraft EULA by modifying eula.txt
* You should see a bunch of output including `[... INFO] [minecraft_rpc]: Listening on 5001`. 
This means it's working and the server is ready for commands on port 5001.

### Calling the server

The interface is defined using [gRPC](https://grpc.io). Read the definition at [src/main/proto/minecraft.proto](src/main/proto/minecraft.proto)

Using the interface definition file you can generate clients for any programming language you like. See [https://grpc.io/docs/languages/](https://grpc.io/docs/languages/)
