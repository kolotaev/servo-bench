#!/usr/bin/env bash

# Defaults
DO_KILL=false
DO_BUILD=false
DO_RUN=false
ATTACHED=false
SQL_SLEEP_MAX=2 # seconds
LOOP_COUNT=100


# Functions
function main() {
    define_image
    build_image
    kill_previous_container
    launch_container
}

function define_image() {
    if [[ -z "$IMAGE" ]]
    then
        echo "++ Working with image name taken from current working directory"
        IMAGE=$(basename $(pwd))
    fi

    NAME="${IMAGE}_container"
}

function build_image() {
    if [[ "$DO_BUILD" = true ]];
    then
        echo "++ Building image..."
        docker build -t ${IMAGE} .
    else
        echo "-- Skip building of image..."
    fi
}

function kill_previous_container() {
    if [[ "$DO_KILL" = true ]];
    then
        echo "++ Killing existing container..."
        docker rm -f "${IMAGE}_container"
    else
        echo "-- Skip killing of previously run container..."
    fi
}

function launch_container() {
    if [[ "$DO_RUN" = true ]];
    then
        CMD="docker run --name=$NAME --rm "

        if [[ "$ATTACHED" = false ]];
        then
            CMD="${CMD} -d "
        fi

        CMD="${CMD} -e SQL_SLEEP_MAX=${SQL_SLEEP_MAX} -e LOOP_COUNT=${LOOP_COUNT}"
        CMD="${CMD} --net=host $IMAGE"

        echo "++ Launching container..."
        eval ${CMD}
    else
        echo "-- Skip running container..."
    fi
}

function show_usage() {
cat << EOF
-------------------------------------------
This script runs docker container for specific framework.
OPTIONS:
   -d      Directory name of the framework service (if not specified, defaults to the current directory)
   -r      Run container? (default: false)
   -b      Build image? (default: false)
   -k      Kill the previously run container? (default: false)
   -a      Attach container's TTY? (default: false)
   -l      Max loop count for service load. Docker container env variable LOOP_COUNT (default: 100)
   -s      Max sleep seconds for DB call. Docker container env variable SQL_SLEEP_MAX (default: 2)
   -h      Show script usage
-------------------------------------------
EOF
}


# Running Main!
while getopts d:p:l:s:ahkbr option
do
    case "${option}"
    in
    d) IMAGE=${OPTARG};;
    r) DO_RUN=true;;
    k) DO_KILL=true;;
    b) DO_BUILD=true;;
    a) ATTACHED=true;;
    l) LOOP_COUNT=${OPTARG};;
    s) SQL_SLEEP_MAX=${OPTARG};;
    h) show_usage; exit;;
    \?) show_usage; exit;;
    esac
done

main
