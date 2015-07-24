import requests
import os
import shutil
import multiprocessing
import random
from config_data.site_config import SiteConfig


def download_file_async(file_name, dest_folder):
    print("Downloading " + file_name + " to " + dest_folder)
    mgr = CacheFileManager(file_name)
    mgr.perform_download()
    print("done")


class CacheFileManager:
    def __init__(self, file):

        config = SiteConfig()

        self.cache_folder = os.path.abspath(config.cache_folder)
        self.file_name = file
        self.full_file_path = os.path.join(self.cache_folder, self.file_name.lower())
        self.download_base_url = config.download_base_url
        self.source_url = self.download_base_url.strip('/') + "/" + self.file_name
        self.local_download_url = "/static/files_cache/" + self.file_name.lower()

        if self.file_name:
            self.file_name = self.file_name.strip()

    @property
    def is_available(self):
        if not self.file_name:
            return False

        file_name = self.file_name.lower().strip()

        # check cache
        local_file = os.path.join(self.cache_folder, file_name)
        available = os.path.exists(local_file)

        print("Using file: " + local_file)

        return available

    def cache_async(self):
        p = multiprocessing.Process(
            target=download_file_async,
            args=(self.file_name, self.cache_folder))
        p.daemon = True
        p.start()

    def perform_download(self):
        if self.is_available:
            return

        print("Would download: " + self.source_url)

        r = requests.get(self.source_url, timeout=5, stream=True)
        if r.status_code != 200:
            print("Bad requests, cancelled..")
            return

        tmp_file = 'tmp__' + ''.join(random.choice('0123456789ABCDEF') for i in range(16)) + "_" + self.file_name
        tmp_out = os.path.join(self.cache_folder, tmp_file)

        try:
            print("Starting download")
            with open(tmp_out, "+wb") as fout:
                shutil.copyfileobj(r.raw, fout)
            print("Data downloaded")

            # check again, could have been downloaded since.
            if self.is_available:
                print("Removing unnecessary tmp file: " + repr(tmp_file))
                if os.path.exists(tmp_out):
                    os.remove(tmp_out)
                return

            print("Moving temp file to live file")
            os.rename(tmp_out, self.full_file_path)
            print("Success for " + self.file_name.lower())

        except Exception as x:

            print("Error downloading file: " + repr(x))
            if os.path.exists(tmp_out):
                os.remove(tmp_out)
