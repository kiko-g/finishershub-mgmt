import os
import sys
import boto3
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


def list_files_in_s3_bucket(game: str):
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    s3 = boto3.client('s3')

    response = s3.list_objects_v2(Bucket=aws_s3_bucket_name)
    if 'Contents' in response:
        for file_obj in response['Contents']:
            file_key = file_obj['Key']
            print(file_key)
    else:
        print("No files found in the S3 bucket.")


def download_from_s3(game: str):
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    s3 = boto3.client('s3')
    folder_path = f"videos/{game}"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    response = s3.list_objects_v2(Bucket=aws_s3_bucket_name)
    if 'Contents' in response:
        for file_obj in response['Contents']:
            file_key = file_obj['Key']
            if file_key.endswith(".mp4"):
                file_path = os.path.join(folder_path, os.path.basename(file_key))
                s3.download_file(aws_s3_bucket_name, file_key, file_path)
                print(colored(f"{file_key} downloaded to {file_path}", "green"))
    else:
        print("No MP4 files found in the S3 bucket.")


def upload_to_s3(game: str):
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    s3 = boto3.client('s3')
    folder_path = f"videos/{game}"

    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as file:
                video_data = file.read()
                s3.put_object(
                    Bucket=aws_s3_bucket_name,
                    Key=f"{game}/{filename}",
                    Body=video_data
                )
            print(colored(f"{filename} uploaded to S3 {aws_s3_bucket_name}", "green"))


def print_usage():
    print(colored("Usage: python s3.py list <mwYYYY>", "red"))
    print(colored("Usage: python s3.py list all", "red"))
    print(colored("Usage: python s3.py upload <mwYYYY>", "red"))
    print(colored("Usage: python s3.py upload all", "red"))
    print(colored("Usage: python s3.py download <mwYYYY>", "red"))
    print(colored("Usage: python s3.py download all", "red"))


if __name__ == "__main__":
    load_dotenv()
    envs = check_envs()
    aws_s3_bucket_prefix = envs["AWS_S3_BUCKET_PREFIX"]
    aws_s3_region_name = envs["AWS_S3_REGION_NAME"]
    aws_access_key_id = envs["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = envs["AWS_SECRET_ACCESS_KEY"]

    s3 = boto3.client('s3',
                      region_name=aws_s3_region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    # operation not specified
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    # list files operation
    elif sys.argv[1] == "list":
        if sys.argv[2] == "all":
            list_files_in_s3_bucket("mw2019")
            list_files_in_s3_bucket("mw2022")

        elif sys.argv[2]:
            game = sys.argv[2]
            if (game == "mw2019" or game == "mw2022"):
                list_files_in_s3_bucket(game)
            else:
                print(colored(f"Game '{game}' does not exist", "red"))
                print_usage()
                sys.exit(1)

    # upload operation
    elif sys.argv[1] == "upload":
        if sys.argv[2] == "all":
            upload_to_s3("mw2019")
            upload_to_s3("mw2022")

        elif sys.argv[2]:
            game = sys.argv[2]
            if (game == "mw2019" or game == "mw2022"):
                upload_to_s3(game)
            else:
                print(colored(f"Game '{game}' does not exist", "red"))
                print_usage()
                sys.exit(1)

    # download operation
    elif sys.argv[1] == "download":
        if sys.argv[2] == "all":
            download_from_s3("mw2019")
            download_from_s3("mw2022")

        elif sys.argv[2]:
            game = sys.argv[2]
            if (game == "mw2019" or game == "mw2022"):
                download_from_s3(game)
            else:
                print(colored(f"Game '{game}' does not exist", "red"))
                print_usage()
                sys.exit(1)

    else:
        print_usage()
        sys.exit(1)
