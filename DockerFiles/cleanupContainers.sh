#!/bin/zsh
docker stop client
docker stop loadbalancer
docker stop worker1
docker stop worker2
docker stop worker3

docker network remove externalNetwork
docker network remove internalNetwork

docker rm client
docker rm loadbalancer
docker rm worker1
docker rm worker2
docker rm worker3
