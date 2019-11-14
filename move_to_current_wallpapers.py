import glob
import os
import shutil
import json


class MoveToCurrentWallpapers:
    def __init__(self):
        self.root_path = ''
        self.current_wallpapers_path = ''
        self.project_path = ''
        self.current_wallpapers_path = ''

    def set_project_path(self, path=None):
        if path is None:
            self.project_path = os.getcwd()
        else:
            self.project_path = path

    def set_current_wallpapers_path(self, path=None):
        if path is None:
            self.current_wallpapers_path = f"{self.root_path}/current_wallpapers"
        else:
            self.current_wallpapers_path = path

    def scan_json(self):
        # get the specified path of the wallpapers
        with open('package.json') as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']

    def get_list_of_existing_wallpapers(self):
        previous_working_directory = os.getcwd()
        os.chdir(self.current_wallpapers_path)
        wallpapers_list = os.listdir()
        os.chdir(previous_working_directory)
        return wallpapers_list

    def create_current_wallpapers_directory(self):
        try:
            os.mkdir(self.current_wallpapers_path)
        except FileExistsError:
            pass

    def copy_all_wallpapers(self):
        os.chdir(self.root_path)

        collection_directories = glob.glob('./*')

        self.create_current_wallpapers_directory()

        current_wallpapers_list = self.get_list_of_existing_wallpapers()

        for directory in collection_directories:
            os.chdir(directory)
            wallpapers = glob.glob('*.jpg')
            for wallpaper in wallpapers:
                if wallpaper not in current_wallpapers_list:
                    try:
                        shutil.copy(wallpaper, self.current_wallpapers_path)
                        print(f'Adding {wallpaper} to current_wallpapers')
                    except shutil.SameFileError:
                        pass

            os.chdir(self.root_path)

    def run(self):
        self.set_project_path()
        self.scan_json()
        self.set_current_wallpapers_path()
        self.copy_all_wallpapers()
        os.chdir(self.project_path)
