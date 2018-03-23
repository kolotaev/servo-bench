IMAGE=$(basename $(pwd))

docker build -t ${IMAGE} .
