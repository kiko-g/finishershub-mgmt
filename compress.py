import os
import sys
from termcolor import colored
from moviepy.editor import VideoFileClip


def compress_videos(game: str):
    source_folder = f"videos/{game}"
    target_folder = f"videos/{game}/compressed"
    os.makedirs(target_folder, exist_ok=True)  # Create the target folder if it doesn't exist

    file_list = [filename for filename in os.listdir(source_folder) if filename.endswith(".mp4")]
    total_files = len(file_list)
    for i, filename in enumerate(file_list, start=1):
        # if i == 2: return
        if os.path.exists(os.path.join(target_folder, filename)):
            print(colored(f"[{i}/{total_files}] {filename} already exists in {target_folder}", "yellow"))
        input_path = os.path.join(source_folder, filename)
        output_path = os.path.join(target_folder, filename)

        video_clip = VideoFileClip(input_path)
        compressed_clip = video_clip.resize(height=720)
        compressed_clip.write_videofile(output_path)
        compressed_clip.close()

        print(colored(f"[{i}/{total_files}] {filename} compressed and saved to {output_path}", "green"))


def print_usage():
    print(colored("Usage: python compress.py <mwYYYY>", "red"))
    print(colored("Usage: python compress.py all", "red"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    elif sys.argv[1] == "all":
        compress_videos("mw2019")
        compress_videos("mw2022")

    elif sys.argv[1]:
        game = sys.argv[1]
        if (game == "mw2019" or game == "mw2022"):
            compress_videos(game)
        else:
            print(colored(f"Game '{game}' does not exist", "red"))
            print_usage()
            sys.exit(1)
