"""
    Cache-tier client allows for querying for files on your cache-tier system.
    These queries can both trigger populating the remote cache as well as
    the client itself can locally store the status of files in memory so as
    to limit the required network traffic and latency of your application.

    Visit https://github.com/mikeckennedy/cache-tier for more details and
    examples. Written by Michael Kennedy @mkennedy
"""

from .cache_client import CacheTierClient
