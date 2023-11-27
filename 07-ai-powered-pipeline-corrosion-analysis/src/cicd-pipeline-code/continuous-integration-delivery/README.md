docker login docker.io -u yoshidj

docker buildx build -o type=docker --platform=linux/amd64 -t yoshidj/pipeline-corr-cicd:serve .

docker push docker.io/yoshidj/pipeline-corr-cicd:serve
