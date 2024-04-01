import os
import pathlib
import re
import shutil

from Video import Video
class VideoManager:
    def __init__(self, main_folder, file_extensions, exclusion_list):
        self.main_folder = main_folder
        self.file_extensions = file_extensions
        self.exclusion_list = exclusion_list
        self.videos = []

    def is_tv_or_movie(self, video):
        if re.search(r'S\d{1,2}E\d{1,2}', str(video)) is not None:
            return "TV"
        else:
            return "Movie"

    def clean_up_name(self, video):
        name = str(video.stem)
        for term in self.exclusion_list:
            name = re.sub(r'\.?\b{}\b\.?'.format(re.escape(term)), '.', name, flags=re.IGNORECASE)
        return name.strip('.').strip()

    def scan_for_videos_and_make_objects(self):
        video_paths = []
        for root, dirs, files in os.walk(self.main_folder):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    video_paths.append(pathlib.Path(root) / file)
        for video in video_paths:
            self.videos.append(Video(path=video, size=video.stat().st_size, type=self.is_tv_or_movie(video), name=self.clean_up_name(video), ext=video.suffix))


    def update_main_folder(self,main_folder):
        self.main_folder = main_folder

    def delete_video_and_folder(self, video):
        video_path = video.path
        try:
            # Delete the video file
            os.remove(video_path)

            # Check if parent directory is not the main folder
            parent_dir = video_path.parent
            if parent_dir != self.main_folder:
                shutil.rmtree(parent_dir)
                print(f"Parent directory {parent_dir} deleted successfully.")

            # Remove the video object from the list
            self.videos.remove(video)
        except Exception as e:
            print(f"Error deleting video and folder: {e}")