#!/bin/bash

if [ $# -ne 1 ]; then
  echo "valid ipam py file required as first argument"
  exit 1
fi

if [ -f ./$1 ]; then
  eval "exec $@"
else
  echo "need first argument to be a valid ipam py file"
  exit 1
fi
