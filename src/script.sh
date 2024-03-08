#!/bin/bash

# Checking the number of parameters
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <file_name.mkv> [-ss <start_time>] [-to <end_time>]"
    exit 1
fi

# Extract parameter for file and its extension
FILE="$1"
EXTENSION="${FILE##*.}"

# Variable initialization for -ss and -to
SS=""
TO=""

# Check file extension
if [ "$EXTENSION" = "mp3" ]; then
    SKIP_CONVERSION="yes"
elif [ "$EXTENSION" = "mkv" ]; then
    SKIP_CONVERSION="no"
else
    echo "Error: Unsupported file type. Please use an MKV or MP3 file."
    exit 1
fi

# Analysis of additional parameters
shift # Deletion of the first argument, which is the file name
while [ "$#" -gt 0 ]; do
    case "$1" in
        -ss)
            SS="$2"
            shift 2
            ;;
        -to)
            TO="$2"
            shift 2
            ;;
        *)
            echo "Option unknown: $1"
            exit 1
            ;;
    esac
done

# Initialization
mkdir -p output

# Convert mkv to mp3 if necessary
if [ "$SKIP_CONVERSION" = "no" ]; then
    python3 src/convertMKVtoMP3.py "$FILE"
    FILE="temp.mp3" # Update FILE to be the converted file
fi

# ffmpeg command to split the audio file
NOW=$(date +"%Y-%m-%d_%H-%M-%S")
FFMPEG_CMD="ffmpeg -i \"$FILE\""

# Add -ss and -to options if defined
if [ ! -z "$SS" ]; then
    FFMPEG_CMD="$FFMPEG_CMD -ss $SS"
fi

if [ ! -z "$TO" ]; then
    FFMPEG_CMD="$FFMPEG_CMD -to $TO"
fi

# Executing the ffmpeg command
FFMPEG_CMD="$FFMPEG_CMD -c copy output/audio_${NOW}.mp3"
eval $FFMPEG_CMD

# Running the meeting minutes script
python3 src/meetingMinutes.py output/audio_${NOW}.mp3

# Cleaning
if [ "$SKIP_CONVERSION" = "no" ]; then
    rm temp.mp3
fi
