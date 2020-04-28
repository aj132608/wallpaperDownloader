import pyunsplash
import requests
import os
import logging
import json
from tkinter import *
from move_to_current_wallpapers import MoveToCurrentWallpapers
from multithreading_download import ThreadingDownload
from remove_mobile_wallpapers import RemoveMobileWallpapers


class WallpaperDownloader:
    def __init__(self):
        self.api_key = ''

        # Paths
        self.root_path = ''
        self.working_directory = os.getcwd()

        # Default user options and states
        self.current_page = 1
        self.photos_per_page = 10
        self.collections_per_page = 10

        # Unsplash Object
        self.un_obj = None

        # Lists
        self.current_collection_list = []
        self.checkbox_objects = []
        self.button_objects = []
        self.checkbox_states = []

        # Styles
        self.background_color = "antique white"
        self.window_size = "450x500"
        self.title = "Wallpaper Downloader"

        # GUI items
        self.root = None
        self.title_frame = None
        self.contents_frame = None
        self.buttons_frame = None
        self.current_title = None

        logging.getLogger("pyunsplash").setLevel(logging.DEBUG)

    def load_from_package(self, file_name='package.json'):

        """

        Loads the data from a specified json file into the following class variables:

        - root_path: directory where the wallpapers will be downloaded (Key Name: root_directory)
        - api_key: api key provided by unsplash.com (Key Name: API_key)
        - photos_per_page: number of photos to be downloaded from each collection (Key Name: wallpapers_per_page)
        - collections_per_page: number of collections displayed on each page (Key Name: collections_per_page)

        :param file_name: You can use any json file name you want here but the default is package.json
        :return: None
        """

        assert os.path.exists(file_name), f"{file_name} does not exist."

        with open(file_name) as json_file:
            data = json.load(json_file)
            self.root_path = data['root_directory']
            self.api_key = data['API_key']
            self.photos_per_page = data['wallpapers_per_page']
            self.collections_per_page = data['collections_per_page']

    def initialize_unsplash_object(self):

        """

        Using the pyunsplash library, this method creates the Pyunsplash object that will be used to access all of the
        collections and photos that the user will navigate through.

        :return: None
        """

        self.un_obj = pyunsplash.PyUnsplash(api_key=self.api_key)

    def update_collection_list(self):

        """

        This method populates current_collection_list with the collections corresponding to the current_page number

        :return: None
        """

        self.current_collection_list = self.un_obj.collections(type_='featured', page=self.current_page,
                                                               per_page=self.collections_per_page)

    def start_gui(self):

        """

        Using the tkinter library, this method creates the Tk object and sets the specs for the GUI window.

        :return: None
        """

        self.root = Tk()
        self.root.geometry(self.window_size)

        self.root.configure(background=self.background_color)

        # Create the Frames
        self.title_frame = Frame(self.root, bg=self.background_color)
        self.contents_frame = Frame(self.root, bd="2px", padx=10, bg=self.background_color)
        self.buttons_frame = Frame(self.root, padx=10, bg=self.background_color)

        # Pack the Frames
        self.title_frame.pack(side=TOP, fill=X)
        self.buttons_frame.pack(fill=X)
        self.contents_frame.pack(side=LEFT, fill=Y)

        # Create the first title for the current collection list
        self.current_title = Label(self.title_frame, text=f"Collection Page {self.current_page}",
                                   bg=self.background_color, fg="black")
        self.current_title.pack(side=TOP)
        self.root.title(self.title)

    def delete_checkboxes(self):

        """

        This method deletes checkbox widgets from the Tk object by iterating through the checkbox object list.

        :return: None
        """

        for checkbox_object in self.checkbox_objects:
            checkbox_object.destroy()

    def create_buttons(self):

        """

        Creates the Button widgets and packs them into the button frame.

        :return: None
        """

        next_page_button = Button(self.buttons_frame, text="-->", command=self.go_to_next_page, bg='white')
        download_button = Button(self.buttons_frame, text="Download", command=self.download, bg='white')
        previous_button = Button(self.buttons_frame, text="<--", command=self.go_to_previous_page, bg='white')

        previous_button.pack(side=LEFT, pady=10)
        download_button.pack(side=LEFT, padx=20, pady=10)
        next_page_button.pack(side=LEFT, pady=10)

    def create_checkboxes(self):

        """

        Creates Checkbuttons for each collection and adds them to the content frame in a grid format.

        :return:
        """

        # Delete all of the elements from checkbox_states so checked boxes from the previous screen don't carry over to
        # the next screen.
        self.checkbox_states.clear()

        # set the first row of the grid, for the checkboxes, to 0
        current_row = 0

        # iterate through the list of collections and add a checkbox for each one
        for collection in self.current_collection_list.entries:
            # these track whether or not the checkboxes are checked
            current_state = IntVar()
            self.checkbox_states.append(current_state)

            # Try setting the collection name as the label of the checkbox
            try:
                # Create the Checkbutton object
                collection_checkbox = Checkbutton(self.contents_frame, text=collection.title, variable=current_state,
                                                  bg=self.background_color, fg="black")

                # Add the Checkbutton object to the current list of Checkbuttons
                self.checkbox_objects.append(collection_checkbox)

                # Place the Checkbutton widget into the specified grid location
                collection_checkbox.grid(row=current_row, columnspan=3, sticky=W)

            # If there is an error due to special characters,
            except Exception as e:
                # Call validate_string to get a title without any special characters outside of the standard ASCII table
                new_title = WallpaperDownloader.validate_string(collection.title)

                # Create the Checkbutton object
                collection_checkbox = Checkbutton(self.contents_frame, text=new_title, variable=current_state,
                                                  bg=self.background_color, fg="black")

                # Add the Checkbutton object to the current list of Checkbuttons
                self.checkbox_objects.append(collection_checkbox)

                # Place the Checkbutton widget into the specified grid location
                collection_checkbox.grid(row=current_row, columnspan=3, sticky=W)

            # iterate current_row so the next Checkbutton will be added in the row below the previous one.
            current_row += 1

    def go_to_next_page(self):

        """

        Add 1 to the current_page class variable,
        updates the title to reflect the new page number,
        deletes the old Checkbuttons,
        updates the list of collections with collections from the new page,
        create new Checkbuttons for the new collection list and add them to the content frame.

        :return: None
        """

        self.current_page += 1
        self.current_title['text'] = f"Collection Page {self.current_page}"
        self.delete_checkboxes()
        self.update_collection_list()
        self.create_checkboxes()

    def go_to_previous_page(self):

        """

        Subtract 1 from the current_page class variable,
        updates the title to reflect the new page number,
        deletes the old Checkbuttons,
        updates the list of collections with collections from the new page,
        create new Checkbuttons for the new collection list and add them to the content frame.

        Won't do anything if the current page is 1.

        :return: None
        """

        if self.current_page > 1:
            self.current_page -= 1
            self.current_title['text'] = f"Collection Page {self.current_page}"
            self.delete_checkboxes()
            self.update_collection_list()
            self.create_checkboxes()

    def download(self):

        """

        This method is called when the download button is pressed and starts the whole download procedure. It iterates
        through the checkbox states and only downloads the collections that were selected.

        :return: None
        """

        index = 0
        for collection in self.current_collection_list.entries:
            if self.checkbox_states[index].get() == 1:
                self.download_collection(collection)
            index += 1

    def download_collection(self, collection):

        """

        Takes in a collection object and downloads a specified number of wallpapers from the collection using
        multi-threading.

        :param collection:
        :return: None
        """

        directory_created = self.make_collection_directory(collection.title)

        threads = []

        if directory_created:
            collection_photos = collection.photos(per_page=self.photos_per_page)

            for photo in collection_photos.entries:
                threads.append(ThreadingDownload(collection.title, photo.link_download, self.root_path, photo.id))

            for thread in threads:
                thread.start()

            print('Collection Successfully Downloaded!\n')

    def __main__(self):
        self.load_from_package()

        self.initialize_unsplash_object()

        self.update_collection_list()

        self.start_gui()

        self.create_buttons()

        self.create_checkboxes()

        self.root.mainloop()

        del self.root

        RemoveMobileWallpapers().run()

        os.chdir(self.working_directory)

        move_wallpapers = MoveToCurrentWallpapers()

        move_wallpapers.run()

        del move_wallpapers

        os.chdir(self.working_directory)

    def make_collection_directory(self, directory_name):

        """

        Creates a directory in the root path and gives it the name that is specified by directory_name

        :param directory_name:
        :return:
        """

        path = f"{self.root_path}{directory_name}"
        try:
            os.mkdir(path)
        except Exception as e:
            print(f"\n\nCreation of {directory_name} failed. Check {path}.\n\n")
            print(e)
            return False
        else:
            print(f"\n\nSuccessfully created {directory_name}.\n\n")
            return True

    @staticmethod
    def validate_string(input_str):

        """

        scan through all characters of the string and only include characters from the standard ASCII library to the
        new string

        :param input_str: a string that may or may not contain special characters
        :return: new_string: input_str without any special characters
        """

        new_string = ""

        for character in input_str:
            if ord(character) < 128:
                new_string += character

        return new_string


WallpaperDownloader().__main__()
