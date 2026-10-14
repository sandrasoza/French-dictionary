#!/bin/bash
#Test input is in the form of string
input="$1" #command argument
if [[ -z "$input" || ! "$input" =~ ^[[:alpha:]]+$ ]]; then
    echo "Error: Invalid input, please enter a valid string."
    exit 1
fi
echo "PASS: valid input, $input"


