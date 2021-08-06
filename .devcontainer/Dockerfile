FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install \
    # Toolchain pakages
    g++-10 libc6-dev binutils \
    cmake ninja-build \
    clang-format clang-tidy \
    git

#Install test framework
RUN git clone https://github.com/cpputest/cpputest.git && \
    mkdir -p cpputest/build && cd cpputest/build && \
    cmake .. -GNinja -DCMAKE_BUILD_TYPE=Release -DC++11=ON -DTESTS=OFF -DVERBOSE_CONFIG=OFF && \
    cmake --build . && cmake --install . && \
    cd ../.. && rm -r cpputest
