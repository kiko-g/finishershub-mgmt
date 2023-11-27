import os
import sys
from termcolor import colored
from moviepy.editor import VideoFileClip, AudioFileClip


def compress_videos(game: str):
    source_folder = f"videos/{game}"
    target_folder = f"videos/{game}/compressed"
    os.makedirs(target_folder, exist_ok=True)  # Create the target folder if it doesn't exist

    file_list = [filename for filename in os.listdir(source_folder) if filename.endswith(".mp4")]
    total_files = len(file_list)

    # compression settings
    skip = True  # Set to True to skip existing files
    limit = None  # Set to None to compress all files
    preset = "fast"  # ultrafast, superfast, faster, fast, medium, slow, veryslow
    threads = 8  # Number of threads to use for compression
    audio_codec = "aac"  # libmp3lame, libvorbis, libopus, aac, pcm_s16le
    bitrate = "5000k"
    codec = "libx264"
    height = 720

    for i, filename in enumerate(file_list, start=1):
        if limit is not None and i > limit:
            new_file_list = [f for f in os.listdir(target_folder) if f.endswith(".mp4")]
            new_total_files = len(new_file_list)
            print(colored(f"Halted compressions for {game} because of limit {limit}", "yellow"))
            print(colored(f"Saved videos in '{target_folder}' ({new_total_files} files)", "blue"))
            return

        print(colored(f"[{i}/{total_files}] Processing {filename}", "blue"))
        if os.path.exists(os.path.join(target_folder, filename)):
            print(colored(f"[{i}/{total_files}] File already exists in '{target_folder}'", "yellow"))
            if skip is True:
                print(colored(f"[{i}/{total_files}] Skipping", "yellow"))
                continue

            overwrite = input(colored("Do you want to overwrite the existing file? (y/n): ", "yellow"))
            if overwrite.lower() != "y":
                continue

        input_path = os.path.join(source_folder, filename)
        output_path = os.path.join(target_folder, filename)

        video_clip = VideoFileClip(input_path)
        audio_clip = AudioFileClip(input_path)

        # Adjust the video parameters for better quality
        video_clip = video_clip.resize(height=height)
        video_clip.write_videofile(
            output_path,
            codec=codec,
            audio=True,
            audio_codec=audio_codec,
            bitrate=bitrate,
            fps=video_clip.fps,
            threads=threads,
            preset="medium",
        )

        # Merge the compressed video with the original audio
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            output_path,
            codec=codec,
            audio=True,
            audio_codec="aac",
            bitrate=bitrate,
            fps=video_clip.fps,
            threads=threads,
            preset=preset,
        )

        final_clip.close()
        video_clip.close()
        audio_clip.close()
        print(colored(f"[{i}/{total_files}] {filename} compressed and saved to {output_path}", "green"))

    new_file_list = [f for f in os.listdir(target_folder) if f.endswith(".mp4")]
    new_total_files = len(new_file_list)
    print(colored(f"Completed compressions for {game}", "green"))
    print(colored(f"Saved videos in '{target_folder}' ({new_total_files} files)", "green"))


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
        if game == "mw2019" or game == "mw2022":
            compress_videos(game)
        else:
            print(colored(f"Game '{game}' does not exist", "red"))
            print_usage()
            sys.exit(1)
