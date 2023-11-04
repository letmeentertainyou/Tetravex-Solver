#!/bin/bash

# This script takes a path to a tetravex.py file for testing, the reason 
# a filepath is required is so that I can time alternate versions of the algorithm
# before pulling them into the main tetravex.py file.

rm -rf __pycache__

t() {
    echo size=$2
    time -p ./$1 -b $2 >/dev/null 2>&1
    echo
}

t $1 3
t $1 4
t $1 5
t $1 6
#t $1 7
#t $1 8


# This script should have an option for whether or not to swallow the output.