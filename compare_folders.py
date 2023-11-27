import os
import filecmp


def compare_folders(dir1, dir2):
    """
    Compare two folders recursively. Files in each folder are assumed to be
    equal if they have the same name and contents.

    :param dir1: First directory path
    :param dir2: Second directory path
    :return: True if the directory trees are the same and
            there were no errors while accessing the directories or files,
            False otherwise.
    """

    # Compare the directories using dircmp
    comparison = filecmp.dircmp(dir1, dir2)

    # Recursively check if subdirectories are the same
    def are_dirs_equal(dcmp):
        if dcmp.left_only or dcmp.right_only or dcmp.diff_files:
            return False
        for sub_dcmp in dcmp.subdirs.values():
            if not are_dirs_equal(sub_dcmp):
                return False
        return True

    return are_dirs_equal(comparison)


if __name__ == "__main__":
    dir1 = "videos/mw2022"
    dir2 = "videos/unmuted/mw2022"
    comparison = compare_folders(dir1, dir2)

    if comparison:
        print("The two folders are identical!")
    else:
        print("The two folders are different!")
