#!/bin/zsh
docker network create -d bridge --subnet 172.40.0.0/16 externalNetwork
docker network create -d bridge --subnet 172.41.0.0/16 internalNetwork

docker create -ti --name client --cap-add=all -v /Users/harvey/ComputerNetworksProject1/Code:/home/Code clientimage /bin/bash

docker create -ti --name loadbalancer --cap-add=all -v /Users/harvey/ComputerNetworksProject1/Code:/home/Code loadbalancerimage /bin/bash

docker create -ti --name worker1 --cap-add=all -v /Users/harvey/ComputerNetworksProject1/Code:/home/Code workerimage /bin/bash
docker create -ti --name worker2 --cap-add=all -v /Users/harvey/ComputerNetworksProject1/Code:/home/Code workerimage /bin/bash
docker create -ti --name worker3 --cap-add=all -v /Users/harvey/ComputerNetworksProject1/Code:/home/Code workerimage /bin/bash

docker network connect internalNetwork worker1
docker network connect internalNetwork worker2
docker network connect internalNetwork worker3
docker network connect internalNetwork loadbalancer

docker network connect externalNetwork loadbalancer
docker network connect externalNetwork client

docker start worker1
docker start worker2
docker start worker3

docker start loadbalancer
docker start client
