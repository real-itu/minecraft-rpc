FROM maven:3.6.3-jdk-8 AS builder
WORKDIR /src
COPY minecraft-rpc /src
RUN mvn compile
RUN mvn package

FROM openjdk:8-jdk-alpine
WORKDIR /server
COPY server-base .
COPY --from=builder src/target/minecraft-rpc-0.0.5.jar mods/
CMD java -jar spongevanilla-1.12.2-7.3.0.jar
