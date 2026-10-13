#!/bin/bash
#Test input is in the form of string
input= $?
if [ $input -ne 0 ]; then
    echo "Error: Invalid input, please enter a valid string."
    exit 1
fi


