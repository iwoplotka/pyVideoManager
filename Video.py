import os
import shutil
import VideoManager


class Video:

    def __init__(self, path, size, video_type, name, ext,metadata):
        self.path = path
        self.size = size
        self.type = video_type
        self.name = name
        self.ext = ext
        self.metadata = metadata


    def __str__(self):
        return f"Path: {self.path}\nSize: {self.size}\nVideo Type: {self.type}\nName: {self.name}\nExtension: {self.ext}\nMetadata: {self.metadata}\n"


