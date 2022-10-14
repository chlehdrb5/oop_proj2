FROM gcc:latest
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp

RUN apt-get update
RUN apt-get upgrade
RUN apt-get install -y cmake

RUN cmake CMakeLists.txt
RUN make

CMD ./oop_proj2

