#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <ipam command>"
  exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

command=$(basename $1 .py)

bash -c $command
