PORT="8080"
ATTACHED=false

while getopts i:ap:l:s: option
do
	case "${option}"
	in
	i) IMAGE=${OPTARG};;
	a) ATTACHED=true;;
	p) PORT=${OPTARG};;
	l) LOOP_COUNT=${OPTARG};;
	s) SQL_SLEEP_MAX=${OPTARG};;
	esac
done

if [[ -z "$IMAGE" ]]
then
	echo "Working with image name taken from current working directory"
	IMAGE=$(basename $(pwd))
fi

NAME="${IMAGE}_container"

CMD="docker run --name=$NAME --rm "
if [[ "$ATTACHED" = false ]];
then
	CMD="${CMD} -d "
fi

CMD="${CMD} -p ${PORT}:8080 -e SQL_SLEEP_MAX=${SQL_SLEEP_MAX} -e LOOP_COUNT=${LOOP_COUNT} --add-host=database:192.168.33.33 $IMAGE"

eval ${CMD}
