from PIL import Image
import os


class RemoveMobileWallpapers:
    def __init__(self):
        self.root_path = ''

    def initialize_root_path(self):
        import json

        with open('package.json') as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']

    def run(self):
        self.initialize_root_path()

        os.chdir(self.root_path)

        folders = os.listdir(self.root_path)

        for folder in folders:
            for wallpaper in os.listdir(folder):
                with Image.open(folder+"/"+wallpaper) as im:
                    width, height = im.size

                if width < height:
                    os.remove(folder+"/"+wallpaper)
                    print(f'Removed {wallpaper} from {folder}.')

        os.chdir(self.root_path)
