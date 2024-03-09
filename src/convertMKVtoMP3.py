import os
import sys
import datetime

import ffmpeg


def convert_mkv_to_mp3(mkv_file_path, name_mp3_file=None):
    """
    Convert an `.mkv` file into an `.mp3` file.
    :param mkv_file_path: Path to the input file (`.mkv`)
    :param name_mp3_file: Name of output audio file (optional)
    :return: Path to the new file
    """
    # Check that the output directory is present
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Creating name of the output file
    if name_mp3_file is None:
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        name_mp3_file = f"{output_dir}/audio_{formatted_date}.mp3"
    else:
        name_mp3_file = f"{output_dir}/{name_mp3_file}.mp3"

    # Attempt to convert the file
    try:
        ffmpeg.input(mkv_file_path).output(name_mp3_file, audio_bitrate='192k').run(overwrite_output=True)
        print(f"The file '{mkv_file_path}' has been successfully converted to '{name_mp3_file}'.")

        return name_mp3_file
    except ffmpeg.Error as e:
        print(f"Conversion error: {e}")
        sys.exit(1)


def cutting_mp3(mp3_file_path, name_mp3_file=None, start_time=None, end_time=None):
    """
    Cutting the audio file to keep just a part of it.
    :param mp3_file_path: Path to the input file (`.mp3`)
    :param name_mp3_file: Name of output audio file (optional)
    :param start_time: Start of cutting time (optional)
    :param end_time: End of cutting time (optional)
    :return: Path to the new file
    """
    # Check that the output directory is present
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Modification of the file converted as a temporary file
    temp_input_mp3_file = mp3_file_path
    if os.path.exists(os.path.join(output_dir, os.path.basename(mp3_file_path))):
        os.rename(mp3_file_path, f"{output_dir}/temp.mp3")
        temp_input_mp3_file = f"{output_dir}/temp.mp3"

    # Creating name of the output file
    if name_mp3_file is None:
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        name_mp3_file = f"{output_dir}/audio_{formatted_date}.mp3"
    else:
        name_mp3_file = f"{output_dir}/{name_mp3_file}.mp3"

    # Attempt to cut the file
    try:
        # Configuring options for ffmpeg
        ffmpeg_options = {}

        if start_time is not None:
            ffmpeg_options['ss'] = start_time

        if end_time is not None:
            ffmpeg_options['to'] = end_time

        # Running ffmpeg with the options configured
        ffmpeg.input(temp_input_mp3_file, **ffmpeg_options).output(name_mp3_file, c='copy').run(overwrite_output=True)
        print(f"The file '{mp3_file_path}' has been successfully cut to '{name_mp3_file}'.")

        # Cleaning
        os.remove(f"{output_dir}/temp.mp3")

        return name_mp3_file
    except ffmpeg.Error as e:
        print(f"Cutting error: {e}")
        sys.exit(1)
