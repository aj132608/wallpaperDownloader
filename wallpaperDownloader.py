from tkinter.ttk import Style

import pyunsplash
import requests
import os
import logging
import json
from tkinter import *
from move_to_current_wallpapers import MoveToCurrentWallpapers


class WallpaperDownloader:
    def __init__(self):
        self.root_path = ''
        self.api_key = ''
        self.photos_per_page = 30
        self.collections_per_page = 15
        self.current_page = 1

        with open('package.json') as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']
            self.api_key = data['API_key']

        self.un_obj = pyunsplash.PyUnsplash(api_key=self.api_key)
        self.current_collection_list = self.un_obj.collections(type_='featured', page=self.current_page,
                                                               per_page=self.collections_per_page)
        self.checkbox_objects = []
        self.button_objects = []
        self.checkbox_states = []
        self.background_color = "antique white"
        self.window_size = "450x500"
        self.root = Tk()
        self.root.geometry(self.window_size)

        self.root.configure(background=self.background_color)

        # Create the Frames
        self.title_frame = Frame(self.root, bg=self.background_color)
        self.contents_frame = Frame(self.root, bd="2px", padx=10, bg=self.background_color)
        # self.input_frame = Frame(self.root, bd="2px", bg=self.background_color)
        self.buttons_frame = Frame(self.root, padx=10, bg=self.background_color)

        # Pack the shit
        self.title_frame.pack(side=TOP, fill=X)
        self.buttons_frame.pack(fill=X)
        self.contents_frame.pack(side=LEFT, fill=Y)

        self.current_title = Label(self.title_frame, text=f"Collection Page {self.current_page}",
                                   bg=self.background_color, fg="black")
        self.current_title.pack(side=TOP)
        self.root.title("Wallpaper Downloader")

        logging.getLogger("pyunsplash").setLevel(logging.DEBUG)

        self.__main__()

        move_wallpapers = MoveToCurrentWallpapers()
        move_wallpapers.run()

    def update_collection_list(self):
        # populate current_collection_list with the collections corresponding to the current_page number
        self.current_collection_list = self.un_obj.collections(type_='featured', page=self.current_page,
                                                               per_page=self.collections_per_page)

    def delete_checkboxes(self):
        for checkbox_object in self.checkbox_objects:
            checkbox_object.destroy()

    def create_buttons(self):
        next_page_button = Button(self.buttons_frame, text="-->", command=self.go_to_next_page, bg='white')
        download_button = Button(self.buttons_frame, text="Download", command=self.download, bg='white')
        previous_button = Button(self.buttons_frame, text="<--", command=self.go_to_previous_page, bg='white')

        previous_button.pack(side=LEFT, pady=10)
        download_button.pack(side=LEFT, padx=20, pady=10)
        next_page_button.pack(side=LEFT, pady=10)

    def create_checkboxes(self):
        self.checkbox_states.clear()
        current_row = 0
        for collection in self.current_collection_list.entries:
            current_state = IntVar()
            self.checkbox_states.append(current_state)
            try:
                collection_checkbox = Checkbutton(self.contents_frame, text=collection.title, variable=current_state,
                                                  bg=self.background_color, fg="black")
                self.checkbox_objects.append(collection_checkbox)
                collection_checkbox.grid(row=current_row, columnspan=3, sticky=W)
            except Exception as e:
                new_title = WallpaperDownloader.validate_string(collection.title)
                collection_checkbox = Checkbutton(self.contents_frame, text=new_title, variable=current_state,
                                                  bg=self.background_color, fg="black")
                self.checkbox_objects.append(collection_checkbox)
                collection_checkbox.grid(row=current_row, columnspan=3, sticky=W)
            current_row += 1

    def go_to_next_page(self):
        self.current_page += 1
        self.current_title['text'] = f"Collection Page {self.current_page}"
        self.delete_checkboxes()
        self.update_collection_list()
        self.create_checkboxes()

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.current_title['text'] = f"Collection Page {self.current_page}"
            self.delete_checkboxes()
            self.update_collection_list()
            self.create_checkboxes()

    def download(self):
        index = 0
        for collection in self.current_collection_list.entries:
            if self.checkbox_states[index].get() == 1:
                self.download_collection(collection)
            index += 1

    def download_collection(self, collection):
        directory_created = self.make_collection_directory(collection.title)

        if directory_created:
            collection_photos = collection.photos(per_page=self.photos_per_page)

            current_photo = 1

            for photo in collection_photos.entries:
                print(f"Downloading wallpaper {current_photo} of {self.photos_per_page} \n")
                self.download_image(collection.title, photo.link_download, photo.id)
                current_photo += 1

            print('\n')

    def __main__(self):
        self.create_buttons()

        self.create_checkboxes()

        self.root.mainloop()

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

    def download_image(self, directory_name, download_link, photo_id=None):
        import time
        import calendar
        if photo_id is None:
            photo_id = calendar.timegm(time.gmtime())

        path = f"{self.root_path}{directory_name}/wallpaper{photo_id}.jpg"
        r = requests.get(url=download_link, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    @staticmethod
    def validate_string(input_str):
        new_string = ""

        # scan through all characters of the string and only include characters
        # from the standard ASCII library to the new string
        for character in input_str:
            if ord(character) < 128:
                new_string += character

        return new_string


WallpaperDownloader()
