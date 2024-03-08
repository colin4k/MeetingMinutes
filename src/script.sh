#!/bin/bash

# Checking the number of parameters
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <nom_fichier.mkv> -ss <début> -to <fin>"
    exit 1
fi

# Parameter extraction
FILE="$1"
SS="$3"  # The start time after -ss
TO="$5"  # The ending time after -to

# Initialization
mkdir -p output

# Convert mkv to mp3
python3 src/convertMKVtoMP3.py "$FILE"

# ffmpeg command to trim the audio file
NOW=$(date +"%Y-%m-%d_%H-%M-%S")
ffmpeg -i temp.mp3 -ss $SS -to $TO -c copy output/audio_${NOW}.mp3

# Running the meeting minutes script
python3 src/meetingMinutes.py output/audio_${NOW}.mp3

# Cleaning
rm temp.mp3
