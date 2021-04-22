# Minecraft RPC
A [gRPC](https://grpc.io) interface for Minecraft

### Starting the modded Minecraft server

* Install Java 1.8 (You can check your version with `java -version`)
  * unix: `sudo apt-get install openjdk-8-jre`
  * osx: [mkyong.com/java/how-to-install-java-on-mac-osx](https://mkyong.com/java/how-to-install-java-on-mac-osx/)  
* Install docker
  * unix: `sudo yum install -y docker`
  * windows and osx: https://www.docker.com/products/docker-desktop

- Run docker
- Go to `minecraft-rpc/server` and start the server delegator with `python server_delegator.py`
- You can start the servers with the example `python example_multi_server_spawn.py`* in `minecraft-rpc/clients/python` 
- You will now be prompted for how many servers you wish to spawn
- Dockers containers will now start to spawn, one for each server.
- When the servers are finished initializing, their gRPC and minecraft ports will be printed.

*It is possible to change the startup parameters for the server on line 33. World type can both be specified as FLAT, which will generate a completely flat level and as DEFAULT which will generate a normal level. MaxHeapSize dictates how much memory in mb each server is allowed.

### Calling the server

The interface is defined using [gRPC](https://grpc.io). Read the definition at [src/main/proto/minecraft.proto](src/main/proto/minecraft.proto)

See [clients](clients) for generated clients and examples.

When connecting a client, use `localhost`(assuming are hosting it on your own machine) and the gRPC port outputted when spawning the servers.

Using the interface definition file you can generate clients for (almost) any programming language you like. See [https://grpc.io/docs/languages/]

### Closing the server(s)

When exiting the server(s), you can use the prompt in the console which spawned them. This will exit the docker containers, BUT not delete them. If you want the docker containers removed, you will have to manually remove them in docker.

(If the servers are not closed correctly, docker will continue to keep them running until closed manually.)



### Alternative way for single server use (no docker required)

- Install Java 1.8 (You can check your version with `java -version`)
  - unix: `sudo apt-get install openjdk-8-jre`
  - osx: [mkyong.com/java/how-to-install-java-on-mac-osx](https://mkyong.com/java/how-to-install-java-on-mac-osx/)  

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
