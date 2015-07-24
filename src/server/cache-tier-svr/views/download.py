from files_utils.filemanager import CacheFileManager
import flask


def handle_download_request(file_name):
    mgr = CacheFileManager(file_name)

    try:
        if not mgr.is_available:
            mgr.cache_async()
            return flask.redirect(mgr.source_url, 302)

        return flask.redirect(mgr.local_download_url)

    except Exception as x:
        print("Cache-Tier: Error handling download request (falling back to source): ".format(repr(x)))
        return flask.redirect(mgr.source_url, 302)
