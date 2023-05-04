MODE=GIT \
    GIT_REPO_URL=https://github.com/scroll-tech/go-ethereum.git \
    COMMIT_HASH=1263e63 \
    BUILD_CMD='make geth'  \
    BUILT_BINARY_REL_PATH=./build/bin/geth \
    CMD_ARGS='--help' \
    python3 ./utils.py