PORT="8080"
DETACHED="yes"

while getopts i:d:p: option
do
	case "${option}"
	in
	i) IMAGE=${OPTARG};;
	d) DETACHED=${OPTARG};;
	p) PORT=${OPTARG};;
	esac
done

if [[ -z $IMAGE ]]
then
	echo "Working with image name taken from current working directory"
	IMAGE=$(basename $(pwd))
fi

NAME="${IMAGE}_container"

CMD="docker run --name=$NAME --rm "
if [[ $DETACHED == "yes" ]]
then
	CMD="${CMD} -d"
fi

CMD="${CMD} $IMAGE -p $PORT:8080"

eval ${CMD}
