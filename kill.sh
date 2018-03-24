IMAGE=$1

if [[ -z "$IMAGE" ]]
then
	echo "Working with image name taken from current working directory"
	IMAGE=$(basename $(pwd))
fi

docker rm -f "${IMAGE}_container"
