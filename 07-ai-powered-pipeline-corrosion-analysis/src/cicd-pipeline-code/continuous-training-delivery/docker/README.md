docker login docker.io -u yoshidj

docker buildx build -o type=docker --platform=linux/amd64 -t yoshidj/pipeline-corr-ctcd:01 .

docker push docker.io/yoshidj/pipeline-corr-ctcd:01
