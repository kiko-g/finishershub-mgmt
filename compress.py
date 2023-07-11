import os
import sys
from termcolor import colored
from moviepy.editor import VideoFileClip, AudioFileClip


def compress_videos(game: str):
    source_folder = f"videos/{game}"
    target_folder = f"videos/{game}/compressed"
    os.makedirs(target_folder, exist_ok=True)  # Create the target folder if it doesn't exist

    limit = 1 # Set to None to compress all files
    file_list = [filename for filename in os.listdir(source_folder) if filename.endswith(".mp4")]
    total_files = len(file_list)

    for i, filename in enumerate(file_list, start=1):
        if (limit == None or i > limit):
            new_file_list = [f for f in os.listdir(target_folder) if f.endswith(".mp4")]
            new_total_files = len(new_file_list)
            print(colored(f"Halted compressions for {game} because of limit {limit}", "yellow"))
            print(colored(f"Saved videos in '{target_folder}' ({new_total_files} files)", "blue"))
            return
            
        print(colored(f"[{i}/{total_files}] Processing {filename}", "blue"))
        if os.path.exists(os.path.join(target_folder, filename)):
            print(colored(f"[{i}/{total_files}] {filename} already exists in {target_folder}", "yellow"))
            overwrite = input(colored("Do you want to overwrite the existing file? (y/n): ", "yellow"))
            if overwrite.lower() != 'y':
                continue

        input_path = os.path.join(source_folder, filename)
        output_path = os.path.join(target_folder, filename)

        video_clip = VideoFileClip(input_path)
        audio_clip = AudioFileClip(input_path)

        # Adjust the video parameters for better quality
        video_clip = video_clip.resize(height=720)
        video_clip.write_videofile(output_path, codec="libx264", audio=True, audio_codec="aac",
                                   bitrate="5000k", fps=video_clip.fps, threads=4, preset="medium")

        # Merge the compressed video with the original audio
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, codec="libx264", audio=True, audio_codec="aac",
                                   bitrate="5000k", fps=video_clip.fps, threads=4, preset="medium")

        final_clip.close()
        video_clip.close()
        audio_clip.close()
        print(colored(f"[{i}/{total_files}] {filename} compressed and saved to {output_path}", "green"))

    new_file_list = [f for f in os.listdir(target_folder) if f.endswith(".mp4")]
    new_total_files = len(new_file_list)
    print(colored(f"Completed compressions for {game}", "blue"))
    print(colored(f"Saved videos in '{target_folder}' ({new_total_files} files)", "blue"))


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
