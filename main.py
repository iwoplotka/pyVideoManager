import os
import pathlib
import pickle
import re
import sys
import threading
import platform
import subprocess
from tkinter import Tk, Canvas, Listbox, Scrollbar, Button, filedialog
import requests
from PIL import Image, ImageTk
from VideoManager import VideoManager

# Function to load poster asynchronously
def load_poster_async(poster_path):
    # Modify the poster path to download a lower resolution image
    poster_path_lower_res = f"https://image.tmdb.org/t/p/w200/{poster_path.split('/')[-1]}"
    # Open and resize the poster image
    poster_image = Image.open(requests.get(poster_path_lower_res, stream=True).raw)
    width, height = poster_image.size
    new_width = 220
    new_height = int((height / width) * new_width)
    poster_image = poster_image.resize((new_width, new_height))
    # Create PhotoImage and display on canvas
    poster_photo = ImageTk.PhotoImage(poster_image)
    canvas.create_image(960, 241, image=poster_photo, tags="poster")
    canvas.image = poster_photo  # Keep a reference to avoid garbage collection

# Function to display TV show metadata
def metadata_display_tv(metadata):
    metadata_text = (
        f"Title: {metadata['original_name']}\n"
        f"Release Date: {metadata['first_air_date']}\n"
        f"Rating: {metadata['vote_average']} / 10\n"
        f"Language: {metadata['original_language']}\n"
        f"Popularity: {metadata['popularity']}\n"
    )
    canvas.create_text(960, 500, anchor="center", text=metadata_text, fill="#1E89B3", font=("Helvetica", 14), tags="info")

# Function to display movie metadata
def metadata_display_movie(metadata):
    metadata_text = (
        f"Title: {metadata['title']}\n"
        f"Release Date: {metadata['release_date']}\n"
        f"Rating: {metadata['vote_average']} / 10\n"
        f"Runtime: {metadata['runtime']} minutes\n"
        f"Language: {metadata['original_language']}\n"
        f"Popularity: {metadata['popularity']}\n"
    )
    canvas.create_text(960, 500, anchor="center", text=metadata_text, fill="#1E89B3", font=("Helvetica", 14), tags="info")

# Function called when a video is selected
def on_select(event):
    canvas.delete("info")  # Clear existing images and metadata from canvas
    selected_index = listbox.curselection()[0]
    selected_video = sorted(manager.videos, key=lambda x: x.video_type)[selected_index]
    poster_url = selected_video.metadata.info()['poster_path']
    poster_path = f"https://image.tmdb.org/t/p/original/{poster_url}"
    metadata = selected_video.metadata.info()  # Get all metadata
    # Load poster asynchronously
    if poster_path:
        threading.Thread(target=load_poster_async, args=(poster_path,)).start()
    else:
        print("No poster available for this video")
    # Display metadata
    if selected_video.video_type == "TV":
        metadata_display_tv(metadata)
    elif selected_video.video_type == "Movie":
        metadata_display_movie(metadata)


# Function to delete a video
def delete_video():
    selected_index = listbox.curselection()[0]
    selected_video = sorted(manager.videos, key=lambda x: x.video_type)[selected_index]
    manager.delete_video_and_folder(selected_video)
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Function to populate the listbox with video names
def populate_listbox():
    for video in manager.videos:
        if video.video_type == "Movie":
            listbox.insert("end", f"🍿 {video.name}")
        elif video.video_type == "TV":
            listbox.insert("end", f"📺 {video.name}")
        else:
            listbox.insert("end", video.name)

# Function to change the main folder
def change_main_folder():
    new_folder_path = filedialog.askdirectory()
    if new_folder_path:
        manager.main_folder = pathlib.Path(new_folder_path)
        with open("main_folder.pkl", "wb") as file:
            pickle.dump(manager.main_folder, file)
        manager.scan_for_videos_and_make_objects()
        python = sys.executable
        os.execl(python, python, *sys.argv)

# Function to play the selected video
def play_video():
    selected_index = listbox.curselection()[0]
    selected_video = sorted(manager.videos, key=lambda x: x.video_type)[selected_index]
    video_path = str(selected_video.path)
    if platform.system() == "Windows":
        os.startfile(video_path)
    else:
        subprocess.Popen(["xdg-open", video_path])

# Main function
if __name__ == "__main__":
    manager = VideoManager()
    manager.scan_for_videos_and_make_objects()

    # Initialize the Tkinter window
    window = Tk()
    window.geometry("1200x837")
    window.configure(bg="#3360B9")
    window.title("Video Manager")

    # Create canvas for UI elements
    canvas = Canvas(
        window,
        bg="#3360B9",
        height=837,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Draw background rectangles and text
    canvas.create_rectangle(164.0, 96.0, 721.0, 741.0, fill="#EAEEF0", outline="")
    canvas.create_rectangle(742.0, 71.0, 1179.0, 765.0, fill="#EAEEF0", outline="")
    canvas.create_text(281.0, 16.0, anchor="nw", text="Video Manager", fill="#FFFFF2", font=("IBMPlexMono SemiBoldItalic", 40))
    canvas.create_text(250.0, 770.0, anchor="nw", text=f"Directory:{manager.main_folder}", fill="#FFFFFF", font=("IBMPlexMono SemiBoldItalic", 16))

    # Load images for buttons
    image_dir = Image.open("image_3.png")
    image_dir = ImageTk.PhotoImage(image_dir)
    image_delete = Image.open("delete.png").resize((70, 70))
    image_delete = ImageTk.PhotoImage(image_delete)
    image_play = Image.open("play.png").resize((70, 70))
    image_play = ImageTk.PhotoImage(image_play)

    # Create buttons
    dir_button = Button(window, bg="#3360B9", image=image_dir, bd=0, highlightthickness=0, command=change_main_folder)
    dir_button.place(x=164, y=750)
    button_delete = Button(window, bd=0, highlightthickness=0, image=image_delete, bg="#EAEEF0", command=delete_video)
    button_delete.place(x=850, y=680)
    button_play = Button(window, bd=0, highlightthickness=0, image=image_play, bg="#EAEEF0", command=play_video)
    button_play.place(x=950, y=680)

    # Sort videos and create listbox
    manager.videos.sort(key=lambda x: x.video_type)
    listbox = Listbox(window, bg="#EAEEF0", bd=0, highlightthickness=0, relief="ridge", font=("Helvetica", 14), width=40, height=20)
    listbox.place(x=200, y=150)

    # Populate listbox and bind events
    populate_listbox()
    listbox.bind("<<ListboxSelect>>", on_select)
    scrollbar = Scrollbar(window, orient="vertical", command=listbox.yview)
    scrollbar.place(x=680, y=150, height=380)
    listbox.config(yscrollcommand=scrollbar.set)

    # Start GUI event loop
    window.mainloop()
