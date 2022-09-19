#!/bin/zsh
docker network remove externalNetwork
docker network remove internalNetwork

docker rm client
docker rm loadbalancer
docker rm worker1
docker rm worker2
docker rm worker3
