import os
import sys
import boto3
from moviepy.editor import *
from termcolor import colored
from dotenv import load_dotenv


def get_bucket_name(prefix: str, game: str):
    return f"{prefix}.{game}"


def check_envs():
    load_dotenv()
    envs = {}
    missing_envs = []
    env_names = ["AWS_S3_BUCKET_PREFIX", "AWS_S3_REGION_NAME", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]

    for variable_name in env_names:
        env_var = os.getenv(variable_name)
        if env_var:
            envs[variable_name] = env_var
        else:
            missing_envs.append(variable_name)

    if len(missing_envs) > 0:
        # warn about missing envs and exit
        print(colored("You need to specify ", color="red"), end="")
        for i, env_name in enumerate(missing_envs):
            separator = " and " if i == len(missing_envs) - 1 else ", "
            print(colored(f"{env_name}{separator}", color="red"), end="")
        print(colored("in your .env file.", color="red"))
        sys.exit(1)

    else:
        return envs


def download_from_s3(game: str):
    skip = True
    s3 = boto3.client("s3")
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    target_folder = f"videos/unmuted/{game}"
    os.makedirs(target_folder, exist_ok=True)  # Create the folder if it doesn't exist

    response = s3.list_objects_v2(Bucket=aws_s3_bucket_name)
    if "Contents" not in response:
        print(colored(f"No MP4 files found in the S3 bucket ({aws_s3_bucket_name})", "red"))

    files = response["Contents"]
    total_files = len(files)
    for i, file in enumerate(files, start=1):
        filename = file["Key"]
        if not filename.endswith(".mp4"):
            continue

        print(colored(f"[{i}/{total_files}] Processing {filename}", "blue"))
        filepath = os.path.join(target_folder, os.path.basename(filename))

        if os.path.exists(filepath):
            print(colored(f"[{i}/{total_files}] File already exists in {target_folder}", "yellow"))
            if skip is True:
                print(colored(f"[{i}/{total_files}] Skipping", "yellow"))
                continue

            overwrite = input(colored("Do you want to overwrite the existing file? (y/n): ", "yellow"))
            if overwrite.lower() != "y":
                continue

        s3.download_file(aws_s3_bucket_name, filename, filepath)
        print(colored(f"{filename} downloaded to '{filepath}'", "green"))


def remove_audio_from_video(video_path, output_path):
    video = VideoFileClip(video_path)
    video_without_audio = video.without_audio()
    video_without_audio.write_videofile(output_path, codec="libx264")


def upload_to_s3(game: str):
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    s3 = boto3.client("s3")
    folder_path = f"videos/muted/{game}"

    filenames = os.listdir(folder_path)
    total_files = len(filenames)

    if total_files == 0:
        print(colored(f"No files found in {folder_path}", "red"))

    for i, filename in enumerate(filenames, start=1):
        if not filename.endswith(".mp4"):
            continue

        filepath = os.path.join(folder_path, filename)
        with open(filepath, "rb") as file:
            video_data = file.read()
            s3.put_object(Bucket=aws_s3_bucket_name, Key=filename, Body=video_data)
        print(colored(f"[{i}/{total_files}] {filename} uploaded to S3 {aws_s3_bucket_name}", "green"))


if __name__ == "__main__":
    load_dotenv()
    envs = check_envs()
    aws_s3_bucket_prefix = envs["AWS_S3_BUCKET_PREFIX"]
    aws_s3_region_name = envs["AWS_S3_REGION_NAME"]
    aws_access_key_id = envs["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = envs["AWS_SECRET_ACCESS_KEY"]

    s3 = boto3.client(
        "s3",
        region_name=aws_s3_region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    games = ["mw2019", "mw2022"]
    # for game in games:
    #     download_from_s3(game)

    # for game in games:
    #     muted_folder = f"videos/muted/{game}"
    #     os.makedirs(muted_folder, exist_ok=True)
    #     for root, _, files in os.walk(f"videos/unmuted/{game}"):
    #         for i, file in enumerate(files):
    #             if file.endswith(".mp4"):
    #                 video_path = os.path.join(root, file)
    #                 muted_video_path = os.path.join(muted_folder, file)
    #                 if os.path.exists(muted_video_path):
    #                     continue
    #                 remove_audio_from_video(video_path, muted_video_path)
    #                 print(colored(f"[{i}] in muted folder", "green"))

    for game in games:
        upload_to_s3(game)
