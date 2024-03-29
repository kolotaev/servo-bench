#!/usr/bin/env bash

# Defaults
DO_KILL=false
DO_BUILD=false
DO_RUN=false
ATTACHED=false
SQL_SLEEP_MAX=2 # seconds
LOOP_COUNT=100
POOL_SIZE=400
TARGET_URL="http://127.0.0.1:9000/sleep"


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

        CMD="${CMD} -e SQL_SLEEP_MAX=${SQL_SLEEP_MAX} -e LOOP_COUNT=${LOOP_COUNT} -e POOL_SIZE=${POOL_SIZE} -e TARGET_URL=${TARGET_URL}"
        CMD="${CMD} --net=host $IMAGE"

        echo "++ Launching container..."
        eval ${CMD}
    else
        echo "-- Skip running container..."
    fi
}

function build_all_images() {
    DO_BUILD=true
    root_test="/shared"
    root=$(pwd)
    if [[ ! "$root" = "$root_test" ]];
    then
        echo "You must be in repo's root dir: ${root_test}"
        echo "current dir is ${root}"
        exit 1
    fi
    image_dirs=$(find . -type f -name 'processname.txt' | sed -r 's|/[^/]+$||' | sort | uniq)
    for f in $image_dirs; do
        echo "cd into ${f}"
        cd "$f"
        echo '----'
        define_image
        build_image
        cd "$root"
        IMAGE=""
    done
}

function show_usage() {
cat << EOF
-------------------------------------------
This script runs docker container for specific framework.
OPTIONS:
   -x      Build docker images for all frameworks (useful for a newly deployed machine)
   -d      Directory name of the framework service (if not specified, defaults to the current directory)
   -r      Run container? (default: $DO_RUN)
   -b      Build image? (default: $DO_BUILD)
   -k      Kill the previously run container? (default: $DO_KILL)
   -a      Attach container's TTY? (default: $ATTACHED)
   -l      Max loop count for service load. Docker container env variable LOOP_COUNT (default: $LOOP_COUNT)
   -s      Max sleep seconds for DB call. Docker container env variable SQL_SLEEP_MAX (default: $SQL_SLEEP_MAX)
   -p      Postgres pool size (min & max). Docker container env variable POOL_SIZE (default: $POOL_SIZE)
   -u      URL to make http requests to (default: $TARGET_URL)
   -h      Show script usage
-------------------------------------------
EOF
}


# Running Main!
while getopts d:p:u:l:s:ahkbrx option
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
    p) POOL_SIZE=${OPTARG};;
    u) TARGET_URL=${OPTARG};;
    x) build_all_images; exit;;
    h) show_usage; exit;;
    \?) show_usage; exit;;
    esac
done

main
