#!/bin/zsh
tar -cvzf Code.tar.gz ../Code/
tar -cvzf HostedFiles.tar.gz ../HostedFiles/
cp Code.tar.gz Client/Code.tar.gz
cp Code.tar.gz LoadBalancer/Code.tar.gz
cp Code.tar.gz Worker/Code.tar.gz
cp HostedFiles.tar.gz Worker/HostedFiles.tar.gz
docker build -t clientimage ./Client
docker build -t loadbalancerimage ./LoadBalancer
docker build -t workerimage ./Worker
