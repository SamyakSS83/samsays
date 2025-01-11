#!/bin/bash

# Path to your ASCII art file
ASCII_FILE="./ascii_output.txt"

# Check if input is provided
if [ -z "$1" ]; then
  echo "Usage: customascii <message>"
  exit 1
fi

# Read the ASCII art file and replace $1 with the message
while IFS= read -r line; do
  # Replace placeholder $1 with the provided message
  echo "${line//\$1/$1}"
done < "$ASCII_FILE"
