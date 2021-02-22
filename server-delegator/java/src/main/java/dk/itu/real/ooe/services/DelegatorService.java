package dk.itu.real.ooe.services;

import dk.itu.real.ooe.DelegatorServiceGrpc.DelegatorServiceImplBase;
import io.grpc.stub.StreamObserver;
import static java.nio.file.StandardCopyOption.*;

import java.io.IOException;

import dk.itu.real.ooe.Delegator.*;

import java.nio.file.CopyOption;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.net.ServerSocket;

public class DelegatorService extends DelegatorServiceImplBase {

    public DelegatorService(){

    }

    @Override
    public void spawnServer(Port request, StreamObserver<Port> responseObserver){
        //Make method for creating dir names
        try {
            Files.copy(Paths.get("ServerBase"), Paths.get("MC1"), COPY_ATTRIBUTES);
        } catch (IOException e) {
            //TODO: Actual logging
            System.out.println("path error");
        }
        ServerSocket tempSocket = new ServerSocket(0);
        int freePort = tempSocket.getLocalPort();
        tempSocket.close();

        //copyServerFIlesFromBase()
        //GRPCport = findEmptyPort()
        //ServerPort = findEmptyPort()
        //configFileWrite(port)
        //startServer()
    }
}
