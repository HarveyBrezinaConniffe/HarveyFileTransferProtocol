#!/bin/zsh
docker build -t clientimage ./Client
docker build -t loadbalancerimage ./LoadBalancer
docker build -t workerimage ./Worker
