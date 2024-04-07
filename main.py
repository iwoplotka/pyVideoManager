import os
import pathlib
import re

from VideoManager import VideoManager

if __name__ == "__main__":
    MAIN_FOLDER = pathlib.Path("/home/iwoplotka/TorrentDownloads")
    FILE_EXTENSIONS = [".mp4", ".mkv"]
    EXCLUSION_LIST =['h264-lazycunts','x264-PHOENiX','WEBRip','x265-RARBG','AMZN','DDP5','Atmos','x264-NOGRP','x264-CM','WEB-DL','BluRay','H264','AAC-RARBG','264-NTb','1','x264-usury','blueray','DSNP','HMAX','x264-NTb','Repack','264-CM','x264-NTb[rartv]','0','DD2','h264-plzproper','WEB','YIFY']

    manager = VideoManager(MAIN_FOLDER, FILE_EXTENSIONS, EXCLUSION_LIST)
    manager.scan_for_videos_and_make_objects()
    for video in manager.videos:
        print(video.metadata.info())


