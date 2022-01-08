import logging
import os
import sys
import configparser
from glob import glob
import shutil


class ModMover:

    def __init__(self, gta_v_folder: str, mods_backup_folder: str, additional_mod_files: list[str]):
        self.additionalModFiles = additional_mod_files
        self.modsBackupFolder = mods_backup_folder
        self.gtaVFolder = gta_v_folder
        os.makedirs(self.modsBackupFolder, exist_ok=True)

    def backup(self):
        files = self.generate_full_mod_files_list(self.gtaVFolder)
        self.move(files, self.modsBackupFolder)

    def restore(self):
        files = self.generate_full_mod_files_list(self.modsBackupFolder)
        self.move(files, self.gtaVFolder)

    def generate_full_mod_files_list(self, directory: str):
        asi_files = glob(os.path.join(directory, "*.asi"))
        mod_files = asi_files
        for mod_file in self.additionalModFiles:
            full_file_path = os.path.join(directory, mod_file)
            if os.path.exists(full_file_path):
                mod_files.append(full_file_path)
        return mod_files

    def move(self, files: list[str], target_dir: str):
        print(f"Moving {len(files)} files to directory {target_dir}")
        for file in files:
            try:
                base_name = os.path.basename(file)
                target_file = os.path.join(target_dir, base_name)
                print(f"Moving file {base_name} to directory {target_dir}")
                shutil.move(file, target_file)
            except:
                logging.exception(f"Exception while moving file {file}  to directory {target_dir}")


if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2 or args[1] not in ["remove", "restore"]:
        print("Usage: python mover.py remove|restore")
        exit()

    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config["DEFAULT"]
    gtaVFolder = config.get("GTAVFolder")
    modsBackupFolder = config.get("modsBackupFolder")
    additionalModFiles = config.get("additionalModFiles").split(",")
    mover = ModMover(gtaVFolder, modsBackupFolder, additionalModFiles)
    op = args[1]
    if op == "remove":
        print("Removing and backing up mods")
        mover.backup()
    else:
        print("Restoring mods")
        mover.restore()
