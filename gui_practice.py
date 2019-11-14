from tkinter import *

check_button_objects = []
check_box_states = []
current_page = 1


def show_checkbutton_vals():
    idx = 1
    for state in check_box_states:
        if state.get() == 1:
            print(f"Option {idx} was selected!")
        idx += 1


def delete_checkboxes():

    for check_button_object in check_button_objects:
        print(check_button_object.destroy())

    check_button_objects.clear()
    check_box_states.clear()


def create_checkboxes():
    delete_checkboxes()

    for i in range(current_page, current_page+14):
        new_state = IntVar()
        check_box_states.append(current_state)
        checkbox = Checkbutton(content_frame, text=str(i), variable=new_state)
        check_button_objects.append(checkbox)
        checkbox.pack()


root = Tk()
root.title("Wallpaper Downloader")

title_frame = Frame(root)
title_frame.pack()
collection_list_label = Label(title_frame, text='Here are the collections that you can download.')
collection_list_label.pack(side="top")

content_frame = Frame(root)
content_frame.pack()
for index in range(1, 15):
    current_state = IntVar()
    check_box_states.append(current_state)
    current_item = Checkbutton(content_frame, text=str(current_page), variable=current_state)
    check_button_objects.append(current_item)
    current_item.pack()
    current_page += 1

button_frame = Frame(root)
button_frame.pack(side="bottom", fill=X)

next_page_button = Button(button_frame, text="Next Page", command=create_checkboxes)
download_button = Button(button_frame, text="Download", command=show_checkbutton_vals)
next_page_button.pack(side="left")
download_button.pack(side="left")

root.mainloop()



