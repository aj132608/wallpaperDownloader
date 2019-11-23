from PIL import Image
import os
import json

wallpapers = []

with open('package.json') as json_file:
    data = json.load(json_file)
    root_path = data['root_directory']

os.chdir(root_path)

folders = os.listdir(root_path)

for folder in folders:
    for wallpaper in os.listdir(folder):
        with Image.open(folder+"/"+wallpaper) as im:
            width, height = im.size

        if width < height:
            os.remove(folder+"/"+wallpaper)
            print(f'Removed {wallpaper} from {folder}.')

os.chdir(root_path)

for wallpaper in wallpapers:
    image = Image.open(wallpaper)
