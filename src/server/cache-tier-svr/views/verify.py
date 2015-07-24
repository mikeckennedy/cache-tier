import flask
from files_utils.filemanager import CacheFileManager


def handle_verify_request(file_name):
    try:
        mgr = CacheFileManager(file_name)

        if not mgr.is_available:
            mgr.cache_async()

        return flask.json.jsonify(
            available=mgr.is_available,
            file=file_name,
            error=False,
            error_msg=None)

    except Exception as x:
        print("Cache-Tier: Error verifying request: ".format(repr(x)))
        return flask.json.jsonify(
            available=False,
            file=file_name,
            error=True,
            error_msg=str(x))
