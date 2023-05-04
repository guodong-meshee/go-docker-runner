#!/usr/bin/env python3
import os

MODE = os.getenv('MODE')
if MODE is None:
    raise ValueError('Invalid MODE environment variable')

if MODE not in ['GIT', 'SRC', 'BINARY']:
    raise ValueError('Invalid MODE environment variable')

BUILD_CMD = os.getenv('BUILD_CMD')
# remove trailing single quote
if BUILD_CMD is not None and BUILD_CMD[-1] == "'":
    BUILD_CMD = BUILD_CMD[:-1]
# remove leading single quote
if BUILD_CMD is not None and BUILD_CMD[0] == "'":
    BUILD_CMD = BUILD_CMD[1:]

if (MODE == 'GIT' or MODE=='SRC') and BUILD_CMD is None:
    raise ValueError('Invalid BUILD_CMD environment variable')

BUILT_BINARY_REL_PATH = os.getenv('BUILT_BINARY_REL_PATH')
if (MODE == 'GIT' or MODE=='SRC') and BUILT_BINARY_REL_PATH is None:
    raise ValueError('Invalid BUILT_BINARY_REL_PATH environment variable')


if MODE == 'GIT':
    GIT_REPO_URL = os.getenv('GIT_REPO_URL')
    COMMIT_HASH = os.getenv('COMMIT_HASH')
    if GIT_REPO_URL is None or COMMIT_HASH is None:
        raise ValueError('Invalid [GIT_REPO_URL] or [COMMIT_HASH] environment variable')
    print(f"Cloning {GIT_REPO_URL} at commit {COMMIT_HASH}")
    # Clone the repo
    os.system(f"git clone {GIT_REPO_URL} /tmp/repo")
    # Checkout the commit
    os.system(f"cd /tmp/repo && git checkout {COMMIT_HASH}")
    SRC_PATH = '/tmp/repo'
    os.environ['SRC_PATH'] = SRC_PATH
    MODE='SRC'
    print(f"Turn to SRC mode at {SRC_PATH}")

if MODE == 'SRC':
    SRC_PATH = os.getenv('SRC_PATH')
    if SRC_PATH is None:
        raise ValueError('Invalid [SRC_PATH] environment variable')
    print(f"Using source code at {SRC_PATH}")
    # Build the source code
    build_cmd = f"cd {SRC_PATH} && {BUILD_CMD}"
    print(f"Building with command: {build_cmd}")
    os.system(build_cmd)
    BINARY_PATH = os.path.join(SRC_PATH, BUILT_BINARY_REL_PATH)
    os.environ['BINARY_PATH'] = BINARY_PATH
    MODE='BINARY'

if MODE == 'BINARY':
    BINARY_PATH = os.getenv('BINARY_PATH')
    if BINARY_PATH is None:
        raise ValueError('Invalid [BINARY_PATH] environment variable')
    print(f"Using binary at {BINARY_PATH}")
    # ls -al binary
    os.system(f"ls -al {BINARY_PATH}")
    # Run the binary
    CMD_ARGS = os.getenv('CMD_ARGS')
    # remove trailing and leading single quote
    if CMD_ARGS is not None and CMD_ARGS[-1] == "'":
        CMD_ARGS = CMD_ARGS[:-1]
    if CMD_ARGS is not None and CMD_ARGS[0] == "'":
        CMD_ARGS = CMD_ARGS[1:]
    if CMD_ARGS is None:
        os.system(f"{BINARY_PATH}")
    else:
        os.system(f"{BINARY_PATH} {CMD_ARGS}")
    