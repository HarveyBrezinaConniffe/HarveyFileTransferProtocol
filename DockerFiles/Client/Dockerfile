FROM python:3.8-slim-buster
WORKDIR /home
RUN apt-get update
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping default-jre 
RUN mkdir /home/Downloads/
ADD Code.tar.gz /home/
CMD ["/bin/bash"]
