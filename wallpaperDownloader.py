import pyunsplash
import requests
import os
import logging
import json
from move_to_current_wallpapers import MoveToCurrentWallpapers


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

        MoveToCurrentWallpapers()

    def __main__(self):
        current_page = 1

        self.scan_collection_page(current_page)

        user_selection = input("That was the last from the page. Would you like to continue? (y/n)")

        while user_selection.upper() in ['Y']:
            # Scan through the next page
            current_page += 1
            self.scan_collection_page(current_page)
            user_selection = input("\nThat was the last from the page. Would you like to continue? (y/n)")

    def scan_collection_page(self, page_num):
        collections_page = self.un_obj.collections(type_='featured',page=page_num, per_page=15)

        for collection in collections_page.entries:
            user_selection = input(f'\nWould you like to download the wallpapers from {collection.title}? (y/n): ')

            if user_selection.upper() in ["Y"]:

                directory_created = self.make_collection_directory(collection.title)

                if directory_created:
                    collection_photos = collection.photos(per_page=30)

                    total_photos = 30
                    current_photo = 1

                    for photo in collection_photos.entries:
                        print(f"Downloading wallpaper {current_photo} of {total_photos} \n")
                        self.download_image(collection.title, photo.link_download)
                        current_photo += 1

                    print('\n')

    def make_collection_directory(self, directory_name):
        path = f"{self.root_path}{directory_name}"
        try:
            os.mkdir(path)
        except OSError:
            print(f"\n\nCreation of {directory_name} failed. Check {path}.\n\n")
            return False
        else:
            print(f"\n\nSuccessfully created {directory_name}.\n\n")
            return True

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
