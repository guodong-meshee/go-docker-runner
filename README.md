# go-docker-runner

Run go code in a docker container as fast as possible.

## Disclaimer

This repo is only for development purpose. It is not production ready for the following reasons:
- Fat docker image

## Features

- Modes supported
    - [MODE=BINARY] From Local Pre-built Binary, 
        - Steps:
            - run the binary
        - Environment variables
            - BINARY_PATH: Mounted binary path (optional when BINARY_URL is provided)
            - CMD_ARGS: Arguments to pass to the binary
    - [MODE=SRC] From a mounted source dir, build and run
        - Steps:
            - build the binary
            - run the binary
        - Extra Environment variables
            - SRC_PATH: Mounted source dir
            - BUILD_COMMAND: Command to build the binary
            - BUILT_BINARY_REL_PATH: Relative path to the built binary from the source root
        - Environment variables same as [MODE=BINARY]
            - CMD_ARGS: Arguments to pass to the binary
    - [MODE=GIT] From git repository with a commit hash provided, 
        - Steps:
            - clone the repo, 
            - checkout the commit hash, 
            - build
            - run
        - Extra Environment variables
            - GIT_REPO_URL: Git repository url
            - COMMIT_HASH: Git commit hash
        - Environment variables same as [MODE=SRC]
            - BUILD_COMMAND: Command to build the binary
            - BUILT_BINARY_REL_PATH: Relative path to the built binary from the source root
            - CMD_ARGS: Arguments to pass to the binary

## Usage

### Run without docker example

```bash
    MODE=GIT \
    GIT_REPO_URL=https://github.com/scroll-tech/go-ethereum.git \
    COMMIT_HASH=1263e63 \
    BUILD_CMD='make geth'  \
    BUILT_BINARY_REL_PATH=./build/bin/geth \
    CMD_ARGS='--help' \
    python3 ./utils.py
```

### Run with docker example

```bash
docker build -t go-docker-runner:local -f Dockerfile .
docker run --rm -it \
    -e MODE=GIT \
    -e GIT_REPO_URL=https://github.com/scroll-tech/go-ethereum.git \
    -e COMMIT_HASH=1263e63 \
    -e BUILD_CMD='make geth' \
    -e BUILT_BINARY_REL_PATH=./build/bin/geth \
    -e CMD_ARGS='--help' \
    go-docker-runner:local
```

### Run with docker compose example locally

update test-docker-compose.yaml file to enable build mode like below

```yaml
  test-node-1:
    # use image directly if you don't want to build the image yourself
    #image: goodbai/go-docker-runner:latest
    build:
      context: .
      dockerfile: Dockerfile
```

```bash
    docker compose -f ./test-docker-compose.yaml down # optional in case of previous run
    docker compose -f ./test-docker-compose.yaml build # only if you want to build the image locally
    docker compose -f ./test-docker-compose.yaml up -d
```

### Run with docker compose 

- Copy the content of [test-docker-compose.yaml](./test-docker-compose.yaml) to your `docker-compose.yaml` file
- Update the environment variables / volumes / ports as per your need
- Run `docker compose up -d`