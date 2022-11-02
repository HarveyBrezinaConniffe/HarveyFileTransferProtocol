#!/bin/zsh
tar -cvzf Code.tar.gz ../Code/
cp Code.tar.gz Client/Code.tar.gz
cp Code.tar.gz LoadBalancer/Code.tar.gz
cp Code.tar.gz Worker/Code.tar.gz
docker build -t clientimage ./Client
docker build -t loadbalancerimage ./LoadBalancer
docker build -t workerimage ./Worker
