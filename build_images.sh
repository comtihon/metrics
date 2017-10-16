#!/bin/bash

function build {
    if [[ ! "$(docker images -q com.metric.$1)" ]]
    then
        echo "building $1"
        mkdir -p services
        cd services && git clone https://github.com/comtihon/metric_$1
        cd metric_$1 && ./gradlew build buildDocker  -x test -x test_integration;\
        cd ../../
    else
        echo "skipping $1 build"
    fi;
}

build assessor
build processor
build receiver
build saver
