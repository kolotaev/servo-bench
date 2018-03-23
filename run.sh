while getopts i:d: option do
	case "${option}"
	in
	i) IMAGE=${OPTARG};;
	d) DETACHED=${OPTARG};;
	esac
done

NAME="${IMAGE}_cont"

CMD = "docker run --name=$NAME --rm "
if [[ -nz $DETACHED ]] then;
	CMD = "${CMD} -d "
fi

CMD = "${CMD} -d $IMAGE -p 8080:8080"

eval ${CMD}
