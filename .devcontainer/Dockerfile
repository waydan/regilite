FROM ubuntu:latest

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install g++-10 cmake ninja-build clang-format git
    # Build and install Catch2 testing framework
    #&& cd ~ && git clone https://github.com/catchorg/Catch2.git \
    #&& cd Catch2 && cmake . -G Ninja -Bbuild -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release\
    #&& cmake --build build/ --target install \
    #&& cd .. && rm -r Catch2

