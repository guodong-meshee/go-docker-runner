docker build -t go-docker-runner:local -f Dockerfile .
docker tag go-docker-runner:local goodbai/go-docker-runner:latest
docker push goodbai/go-docker-runner:latest
docker run --rm -it \
    -e MODE=GIT \
    -e GIT_REPO_URL=https://github.com/scroll-tech/go-ethereum.git \
    -e COMMIT_HASH=1263e63 \
    -e BUILD_CMD='make geth' \
    -e BUILT_BINARY_REL_PATH=./build/bin/geth \
    -e CMD_ARGS='--help' \
    go-docker-runner:local
