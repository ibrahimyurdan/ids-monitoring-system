FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    tcpdump \
    iptables \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
CMD ["bash"] 