import ffmpeg
import sys


def convert_mkv_to_mp3(mkv_file, mp3_file):
    """
    Convert an MKV file into an MP3 file.
    :param mkv_file: Input MKV file path
    :param mp3_file: Output MP3 file path
    """
    try:
        # Exécute la conversion
        ffmpeg.input(mkv_file).output(mp3_file, audio_bitrate='192k').run()
        print(f"The file '{mkv_file}' has been successfully converted to '{mp3_file}'.")
    except ffmpeg.Error as e:
        print(f"Conversion error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convertMKVtoMP3.py <mkv_file>")
        sys.exit(1)

    mkv_file = sys.argv[1]

    convert_mkv_to_mp3(mkv_file, "temp.mp3")
