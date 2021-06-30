FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install \
    # Toolchain pakages
    g++-10 \
    build-essential \
    cmake \
    ninja-build \
    clang-format \
    git \
    cpputest
