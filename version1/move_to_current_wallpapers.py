import glob
import os
import shutil
import json


class MoveToCurrentWallpapers:
    def __init__(self):
        self.root_path = ''
        self.current_wallpapers_path = ''

        # get the specified path of the wallpapers
        with open('package.json') as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']

        self.current_wallpapers_path = f"{self.root_path}/current_wallpapers"

        self.copy_all_wallpapers()

    def create_current_wallpapers_directory(self):
        try:
            os.mkdir(self.current_wallpapers_path)
        except FileExistsError:
            print('current_wallpapers already exists.')

    def copy_all_wallpapers(self):
        os.chdir(self.root_path)

        collection_directories = glob.glob('./*')

        self.create_current_wallpapers_directory()

        for directory in collection_directories:
            os.chdir(directory)
            wallpapers = glob.glob('*.jpg')
            for wallpaper in wallpapers:
                try:
                    shutil.copy(wallpaper, self.current_wallpapers_path)
                except shutil.SameFileError:
                    print(f"{wallpaper} already exists!")

            os.chdir(self.root_path)
