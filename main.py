import os
import pathlib
import re
from tkinter import Tk, Canvas, PhotoImage, Listbox, Scrollbar
import requests
from PIL import Image, ImageTk
from VideoManager import VideoManager
import threading


def load_poster_async(poster_path):
    # Modify the poster path to download a lower resolution image
    poster_path_lower_res = f"https://image.tmdb.org/t/p/w200/{poster_path.split('/')[-1]}"

    poster_image = Image.open(requests.get(poster_path_lower_res, stream=True).raw)
    # Calculate new dimensions while maintaining aspect ratio
    width, height = poster_image.size
    new_width = 220
    new_height = int((height / width) * new_width)
    poster_image = poster_image.resize((new_width, new_height))
    poster_photo = ImageTk.PhotoImage(poster_image)
    canvas.create_image(
        960,
        241,
        image=poster_photo,
        tags="poster"
    )
    canvas.image = poster_photo  # Keep a reference to avoid garbage collection


def metadata_display_tv(metadata):
    # Extract and display metadata under the poster
    metadata_text = f"Title: {metadata['original_name']}\n"
    metadata_text += f"Release Date: {metadata['first_air_date']}\n"
    metadata_text += f"Rating: {metadata['vote_average']} / 10\n"
    metadata_text += f"Language: {metadata['original_language']}\n"
    metadata_text += f"Popularity: {metadata['popularity']}\n"

    canvas.create_text(
        960,
        500,
        anchor="center",
        text=metadata_text,
        fill="#1E89B3",
        font=("Helvetica", 14),
        tags="info")




def metadata_display_movie(metadata):
    # Extract and display metadata under the poster
    metadata_text = f"Title: {metadata['title']}\n"
    metadata_text += f"Release Date: {metadata['release_date']}\n"
    metadata_text += f"Rating: {metadata['vote_average']} / 10\n"
    metadata_text += f"Runtime: {metadata['runtime']} minutes\n"
    metadata_text += f"Language: {metadata['original_language']}\n"
    metadata_text += f"Popularity: {metadata['popularity']}\n"

    canvas.create_text(
        960,
        500,
        anchor="center",
        text=metadata_text,
        fill="#1E89B3",
        font=("Helvetica", 14),
        tags="info"
    )


def on_select(event):
    # Clear existing images and metadata from canvas
    canvas.delete("info")

    # Get selected video
    selected_index = listbox.curselection()[0]
    selected_video = sorted(manager.videos, key=lambda x: x.video_type)[selected_index]

    # Load poster image and metadata from video metadata
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


def populate_listbox():
    for video in manager.videos:
        # Determine background color or icon based on video type
        if video.video_type == "Movie":
            listbox.insert("end", f"🍿 {video.name}")
        elif video.video_type == "TV":
            listbox.insert("end", f"📺 {video.name}")  # Prefix TV shows with an icon
        else:
            listbox.insert("end", video.name)  # Default behavior


if __name__ == "__main__":
    MAIN_FOLDER = pathlib.Path("/home/iwoplotka/TorrentDownloads")
    FILE_EXTENSIONS = [".mp4", ".mkv"]
    EXCLUSION_LIST = ['h264-lazycunts', 'x264-PHOENiX', 'WEBRip', 'x265-RARBG', 'AMZN', 'DDP5', 'Atmos', 'x264-NOGRP',
                      'x264-CM', 'WEB-DL', 'BluRay', 'H264', 'AAC-RARBG', '264-NTb', '1', 'x264-usury', 'blueray',
                      'DSNP', 'HMAX', 'x264-NTb', 'Repack', '264-CM', 'x264-NTb[rartv]', '0', 'DD2', 'h264-plzproper',
                      'WEB', 'YIFY']

    window = Tk()
    window.geometry("1200x837")
    window.configure(bg="#3360B9")
    window.title("Video Manager")

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

    # Define colors for left and right rectangles
    color_left = "#1E89B3"
    color_right = "#51AEDF"

    # Calculate colors for linear transition
    num_steps = 100
    colors = [(int((1 - i / num_steps) * int(color_left[1:], 16) + (i / num_steps) * int(color_right[1:], 16))) for i in
              range(num_steps)]
    colors = ['#' + format(c, '06x') for c in colors]

    # Draw rounded grey rectangles
    canvas.create_rectangle(
        164.0,
        96.0,
        721.0,
        741.0,
        fill="#EAEEF0",
        outline=""
    )
    canvas.create_rectangle(
        742.0,
        71.0,
        1179.0,
        765.0,
        fill="#EAEEF0",
        outline=""
    )

    # Draw other elements
    canvas.create_text(
        281.0,
        16.0,
        anchor="nw",
        text="Video Manager",
        fill="#FFFFF2",
        font=("IBMPlexMono SemiBoldItalic", 40)
    )

    canvas.create_text(
        281.0,
        765.0,
        anchor="nw",
        text="Directory:",
        fill="#FFFFFF",
        font=("IBMPlexMono SemiBoldItalic", 24)
    )

    # Add other elements like images
    image_1 = Image.open("image_1.png")
    image_1 = ImageTk.PhotoImage(image_1)
    canvas.image_1 = canvas.create_image(
        960.0,
        241.0,
        image=image_1
    )

    image_3 = Image.open("image_3.png")
    image_3 = ImageTk.PhotoImage(image_3)
    canvas.create_image(
        216.0,
        778.0,
        image=image_3
    )

    # Create VideoManager instance and scan for videos
    manager = VideoManager(MAIN_FOLDER, FILE_EXTENSIONS, EXCLUSION_LIST)
    manager.scan_for_videos_and_make_objects()

    # Sort videos by video_type
    manager.videos.sort(key=lambda x: x.video_type)

    # Create Listbox to display video names
    listbox = Listbox(
        window,
        bg="#EAEEF0",
        bd=0,
        highlightthickness=0,
        relief="ridge",
        font=("Helvetica", 14),
        width=40,
        height=20
    )
    listbox.place(x=200, y=150)

    # Populate Listbox with video names and color based on video_type
    populate_listbox()

    # Bind event for selecting a video
    listbox.bind("<<ListboxSelect>>", on_select)

    # Add scrollbar for Listbox
    scrollbar = Scrollbar(window, orient="vertical", command=listbox.yview)
    scrollbar.place(x=680, y=150, height=380)

    # Link scrollbar to Listbox
    listbox.config(yscrollcommand=scrollbar.set)

    # Start GUI event loop
    window.mainloop()
