docker login docker.io -u yoshidj

docker buildx build -o type=docker --platform=linux/amd64 -t yoshidj/energy-grid-a2b:01 .

docker push docker.io/yoshidj/energy-grid-a2b:01