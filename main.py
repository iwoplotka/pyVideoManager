import os
import pathlib
import re

from Video import Video

MAIN_FOLDER = pathlib.Path("/home/iwoplotka/TorrentDownloads")
FILE_EXTENSIONS = [".mp4", ".mkv"]
EXCLUSION_LIST =['h264-lazycunts','x264-PHOENiX','WEBRip','x265-RARBG','AMZN','DDP5','Atmos','x264-NOGRP','x264-CM','WEB-DL','BluRay','H264','AAC-RARBG','264-NTb','1','x264-usury','blueray','DSNP','HMAX','x264-NTb','Repack','264-CM','x264-NTb[rartv]','0','DD2','h264-plzproper','WEB','YIFY']



def is_tv_or_movie(video): #determines if its a video or a movie
    if re.search(r'S\d{1,2}E\d{1,2}', str(video)) is not None:
        return "TV"
    else:
        return "Movie"



def clean_up_name(video):  #cleans up the name of the file
    name = str(video.stem)  # Get the filename without extension
    for term in EXCLUSION_LIST:
        # Adjusted regular expression to remove exact matches of terms and any surrounding dots
        name = re.sub(r'\.?\b{}\b\.?'.format(re.escape(term)), '.', name, flags=re.IGNORECASE)
    return name.strip('.').strip()  # Strip any extra dots and whitespace from both ends of the name




def scan_for_videos_and_make_objects(folder): #makes a list of objects form video files found
    video_paths = []
    video_objects =[]
    for root, dirs, files in os.walk(folder):#looks for videos
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                video_paths.append(pathlib.Path(root) / file)
    for video in video_paths: #creates an obj
        video_objects.append(Video(path=video, size=video.stat().st_size, type=is_tv_or_movie(video), name=clean_up_name(video), ext=video.suffix))
    return video_objects


video_list = scan_for_videos_and_make_objects(MAIN_FOLDER)
for video in video_list:
    print(vars(video))
