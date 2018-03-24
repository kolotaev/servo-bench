PORT="8080"
ATTACHED=false

while getopts i:a:p: option
do
	case "${option}"
	in
	i) IMAGE=${OPTARG};;
	a) ATTACHED=true;;
	p) PORT=${OPTARG};;
	esac
done

if [[ -z "$IMAGE" ]]
then
	echo "Working with image name taken from current working directory"
	IMAGE=$(basename $(pwd))
fi

NAME="${IMAGE}_container"

CMD="docker run --name=$NAME --rm "
if [[ ! $ATTACHED ]]
then
	CMD="${CMD} -d "
fi

CMD="${CMD} -p ${PORT}:8080 $IMAGE"

eval ${CMD}
