#!/bin/bash
# Parses proto files and generates/regenerates python gRPC modules for all
# protos/service files found.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PROTO_DIR=$SCRIPT_DIR/protos/
OUTPUT_DIR=$SCRIPT_DIR

python3 -m grpc_tools.protoc \
    -I$PROTO_DIR \
    --python_out=$OUTPUT_DIR \
    --grpc_python_out=$OUTPUT_DIR $PROTO_DIR*.proto