from collections import defaultdict
import os
from datetime import timedelta, datetime
import requests

class CacheTierClient:
    """
    Cache-tier client allows for querying for files on your cache-tier system.
    These queries can both trigger populating the remote cache as well as
    the client itself can locally store the status of files in memory so as
    to limit the required network traffic and latency of your application.
    """
    __remote_status_cache = defaultdict()

    def __init__(self, base_url,
                 request_timeout=1.0,
                 enable_local_cache=True,
                 local_cache_time=120.0):
        """
        Cache-tier client allows for querying for files on your cache-tier system.
        These queries can both trigger populating the remote cache as well as
        the client itself can locally store the status of files in memory so as
        to limit the required network traffic and latency of your application.

        :param base_url: The base url of your remove cache-tier system (e.g. http://server/cacheapp/)
        :param request_timeout: Request timeout (in seconds) for communicating with the cache-tier system
        :param enable_local_cache: Should this client instance store the results of a cache query and reuse it for a period of time?
        :param local_cache_time: The period of time (in seconds) between communication with cache-tier system (per file)
        """

        self.local_cache_time = local_cache_time
        """ The period of time between communication with cache-tier system (per file) """

        self.enabled = enable_local_cache
        """ Should this client instance store the results of a cache query and reuse it for a period of time? """

        self.request_timeout = request_timeout
        """ Request timeout (in seconds) for communicating with the cache-tier system """

        self.base_url = base_url.strip().strip('/') + '/'
        """ The base url of your remove cache-tier system (e.g. http://server/cacheapp/) """

    def verify_file(self, file_name):
        """
        Contacts the remove cache-tier system and determines whether the requested file is present on the cache.

        :param file_name: The filename of the remote system. (e.g. video.mp4)
        :return: True or False based on whether the server is accessible and the file is present
         
        """
        self.__validate_file_name(file_name)
        file_name = os.path.basename(file_name.strip())

        if not self.enabled:
            print("CacheClient: Skipping cache server (disabled)")
            return self.__get_server_status(file_name)

        if self.is_stale(file_name):
            print("CacheClient: {} is stale, updating from server".format(file_name))
            available = self.__get_server_status(file_name)
            self.__update_verify_time(file_name, available)
            print("CacheClient: {} availability is {}".format(file_name, available))
            return available

        time, status = CacheTierClient.__remote_status_cache.get(
            file_name.lower(), (None, False))
        print("CacheClient: Using cached for {}, available: {}".format(file_name, status))
        return status

    @staticmethod
    def __update_verify_time(file_name, available):
        name = file_name.lower()
        CacheTierClient.__remote_status_cache[name] = (datetime.now(), available)

    def is_stale(self, file_name):
        """
        Determines whether the cache-tier server should be contacted to
        refresh information about the availability of this file based on
        the set cache usage and timings.

        :param file_name: The base file name (e.g. episode.mp3)
        :return: True of False whether the file info needs refreshed.
        """
        self.__validate_file_name(file_name)
        file_name = os.path.basename(file_name.strip())

        if not self.enabled:
            return True

        item = CacheTierClient.__remote_status_cache.get(
            file_name.lower(), (None, False))

        last_request, available = item
        if last_request is None:
            return True

        dt = timedelta(seconds=self.local_cache_time)
        valid_range = last_request + dt
        return valid_range < datetime.now()

    def __build_verify_url(self, file_name):
        self.__validate_file_name(file_name)
        file_name = os.path.basename(file_name.strip())

        return self.base_url + "verify/" + file_name

    def build_download_url(self, file_name):
        """
        Generates a URL which can be sent to the client (e.g. web browser) to
        download a file from the cache-tier. You should always call verify_file()
        first and only use the download URL if the file has been verified.
        Otherwise, while the cache is building, use the source URL.

        :param file_name: The base file name (e.g. episode.mp3)
        :return: A string representing a URL which points to the cache-tier file.
        """
        self.__validate_file_name(file_name)

        return self.base_url + "download/" + file_name

    # noinspection PyMethodMayBeStatic
    def __validate_file_name(self, file_name):
        if not file_name or not file_name.strip():
            raise CacheException("Invalid filename: {}".format(file_name))

    def __get_server_status(self, file_name):
        try:
            url = self.__build_verify_url(file_name)

            r = requests.get(url, timeout=self.request_timeout)
            result = r.json()

            if result["error"]:
                print("CacheClient: Error returned from cache server " + result["error_msg"])

            return result['available']
        except Exception as x:
            print("CacheClient: Error accessing cache server: {}".format(x))
            return False


class CacheException(Exception):
    """
        The exception type indicating an error with the Cache Tier Client
    """
    pass
