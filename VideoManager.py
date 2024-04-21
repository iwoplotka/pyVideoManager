import os
import pathlib
import pickle
import re
import shutil
import tmdbsimple as tmdb


from Video import Video

tmdb.API_KEY = "ddf06dec75894ad70d54de116951c8ef"
FILE_EXTENSIONS = [".mp4", ".mkv"]
EXCLUSION_LIST = ['x264-PHOENiX', 'WEBRip', 'x265-RARBG', 'AMZN', 'DDP5', 'Atmos', 'x264-NOGRP',
                      'x264-CM', 'WEB-DL', 'BluRay', 'H264', 'AAC-RARBG', '264-NTb', '1', 'x264-usury', 'blueray',
                      'DSNP', 'HMAX', 'x264-NTb', 'Repack', '264-CM', 'x264-NTb[rartv]', '0', 'DD2', 'h264-plzproper',
                      'WEB', 'YIFY']
class VideoManager:
    def __init__(self):
        self.load_main_folder()
        self.file_extensions = FILE_EXTENSIONS
        self.exclusion_list = EXCLUSION_LIST
        self.videos = []

    def load_main_folder(self):
        global main_folder
        if os.path.exists("main_folder.pkl"):
            with open("main_folder.pkl", "rb") as file:
                self.main_folder = pickle.load(file)

        else:
            self.main_folder = pathlib.Path("")

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
            self.videos.append(Video(path=video, size=video.stat().st_size, video_type=self.is_tv_or_movie(video), name=self.clean_up_name(video), ext=video.suffix,metadata=self.get_metadata(video)))

    def clean_name_for_search(self,video):
        name = str(video.stem)
        match = re.search(r'\d{4}|S\d{1,2}E\d{1,2}', name,flags=re.IGNORECASE)
        if match:
            clean_name = name[:match.start()]
        else:
            clean_name = name

        return clean_name.strip('.').strip().replace('.', ' ')

    def get_metadata(self,video):
        try:
            query=self.clean_name_for_search(video)
            print(query)
            if self.is_tv_or_movie(video)=="Movie":
                search = tmdb.Search()
                response = search.movie(query=query)
                return tmdb.Movies(search.results[0]['id'])
            else:
                search = tmdb.Search()
                response = search.tv(query=query)
                return tmdb.TV(search.results[0]['id'])
        except:
            pass


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

