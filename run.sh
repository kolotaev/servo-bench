#!/usr/bin/env bash

PORT="8080"
ATTACHED=false
SQL_SLEEP_MAX=2 # seconds
LOOP_COUNT=100
RERUN=false

while getopts i:arp:l:s: option
do
	case "${option}"
	in
	i) IMAGE=${OPTARG};;
	a) ATTACHED=true;;
	p) PORT=${OPTARG};;
	l) LOOP_COUNT=${OPTARG};;
	s) SQL_SLEEP_MAX=${OPTARG};;
	r) RERUN=true;;
	esac
done

if [[ -z "$IMAGE" ]]
then
	echo "Working with image name taken from current working directory"
	IMAGE=$(basename $(pwd))
fi

NAME="${IMAGE}_container"


# todo - use kill/build script
if [[ "$RERUN" = true ]];
then
    echo "Building image..."
    docker build -t ${IMAGE} .
    echo "Killing existing container..."
    docker rm -f "${IMAGE}_container"
fi


echo "Launching container..."
CMD="docker run --name=$NAME --rm "
if [[ "$ATTACHED" = false ]];
then
	CMD="${CMD} -d "
fi

CMD="${CMD} -p ${PORT}:8080 -e SQL_SLEEP_MAX=${SQL_SLEEP_MAX} -e LOOP_COUNT=${LOOP_COUNT} --add-host=database_host:192.168.33.33 $IMAGE"

eval ${CMD}
