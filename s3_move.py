import os
import boto3
from termcolor import colored
from dotenv import load_dotenv

def get_bucket_name(prefix: str, game: str):
    return f"{prefix}.{game}"

def check_envs():
    load_dotenv()
    envs = {}
    env_names = ["AWS_S3_BUCKET_PREFIX", "AWS_S3_REGION_NAME", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]

    for variable_name in env_names:
        env_var = os.getenv(variable_name)
        if env_var:
            envs[variable_name] = env_var
        else:
            print(colored(f"You need to specify {variable_name} in your .env file.", color="red"))
            exit(1)
    return envs

def move_files_to_root_in_s3_bucket(game: str):
    aws_s3_bucket_name = get_bucket_name(aws_s3_bucket_prefix, game)
    response = s3.list_objects_v2(Bucket=aws_s3_bucket_name)

    if 'Contents' not in response:
        print(colored(f"No files found in the S3 bucket {aws_s3_bucket_name}", "red"))
        return

    for file_obj in response['Contents']:
        file_key = file_obj['Key']
        # If it's in a sub-directory
        if '/' in file_key:
            new_file_key = os.path.basename(file_key)
            # Copy to root
            s3.copy_object(Bucket=aws_s3_bucket_name, CopySource={'Bucket': aws_s3_bucket_name, 'Key': file_key}, Key=new_file_key)
            # Delete original file
            s3.delete_object(Bucket=aws_s3_bucket_name, Key=file_key)
            print(colored(f"Moved {file_key} to root of {aws_s3_bucket_name}", "green"))

if __name__ == "__main__":
    envs = check_envs()
    aws_s3_bucket_prefix = envs["AWS_S3_BUCKET_PREFIX"]
    aws_s3_region_name = envs["AWS_S3_REGION_NAME"]
    aws_access_key_id = envs["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = envs["AWS_SECRET_ACCESS_KEY"]

    s3 = boto3.client('s3',
                      region_name=aws_s3_region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    # Move files for both buckets
    move_files_to_root_in_s3_bucket("mw2019")
    move_files_to_root_in_s3_bucket("mw2022")
