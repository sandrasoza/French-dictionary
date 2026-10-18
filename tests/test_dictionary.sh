#!/bin/bash
#Test: input is in the form of string
input="$*" #command argument

if [[ -z "$input" || ! "$input" =~ ^[[:alpha:]]+([[:space:]]+[[:alpha:]]+)*$ ]]; then
    echo "[Error]: Invalid input, please enter a valid string."
    exit 1
fi
echo "[PASS]: valid input, $input"

#Test: string input accepts more than 1 word
word_count=$(wc -w <<< "$input")
if ((word_count > 1)); then 
    echo "[PASS]: the string has more than one word"
else 
    echo "[PASS]: the string has one word"
fi 
