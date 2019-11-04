import pyunsplash
import requests
import os
import logging
import json


class WallpaperDownloader:
    def __init__(self):
        self.root_path = ''
        self.api_key = ''

        with open('package.json') as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']
            self.api_key = data['API_key']

        self.un_obj = pyunsplash.PyUnsplash(api_key=self.api_key)

        logging.getLogger("pyunsplash").setLevel(logging.DEBUG)

        self.__main__()

    def __main__(self):
        collections_page = self.un_obj.collections(type_='featured', per_page=15)

        for collection in collections_page.entries:
            user_selection = input(f'\nWould you like to download the wallpapers from {collection.title}? (y/n): ')

            if user_selection.upper() in ["Y"]:
                print('\nHere are your download links. \n')

                self.make_directory(collection.title)

                collection_photos = collection.photos(per_page=30)

                for photo in collection_photos.entries:
                    print(f"Downloading wallpaper from {photo.link_download} \n")
                    self.download_image(collection.title, photo.link_download)

                print('\n')

    def make_directory(self, directory_name):
        path = f"{self.root_path}{directory_name}"
        try:
            os.mkdir(path)
        except OSError:
            print(f"\n\nCreation of {directory_name} failed. Check {path}.\n\n")
        else:
            print(f"\n\nSuccessfully created {directory_name}.\n\n")

    def download_image(self, directory_name, download_link):
        import time
        import calendar
        photo_id = calendar.timegm(time.gmtime())

        path = f"{self.root_path}{directory_name}/wallpaper{photo_id}.jpg"
        r = requests.get(url=download_link, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)


WallpaperDownloader()
