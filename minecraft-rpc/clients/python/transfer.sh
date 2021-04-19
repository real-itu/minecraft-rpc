#!/bin/bash
OUTPUTFOLDER="output"
mkdir -p $OUTPUTFOLDER
containers=$(docker ps -a -q)
pushd $OUTPUTFOLDER
for container in $containers
do
    docker logs "$container" > "$container.txt"
done
popd