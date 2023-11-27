import os

base_dir = "videos/muted"
sub_dirs = ["mw2019", "mw2022"]

for sub_dir in sub_dirs:
    full_path = os.path.join(base_dir, sub_dir)
    for file in os.listdir(full_path):
        if file.endswith(".mp4"):
            new_name = f"{sub_dir}_{file}"
            os.rename(os.path.join(full_path, file), os.path.join(base_dir, new_name))
