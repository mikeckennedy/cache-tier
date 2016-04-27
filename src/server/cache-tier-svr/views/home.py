# import sys
# from config_data.site_config import SiteConfig


def handle_home_request():
    # config = SiteConfig()
    # is_prod = SiteConfig.deploy_is_production()

    return ('<meta http-equiv="refresh" content="10; url=http://YOURSERVER.com/">' +
            'Cache-Tier Caching server.<br><br>' +
            'Verify a file using /verify/FILENAME.EXT<br>' +
            'Get download URL of a file using /download/FILENAME.EXT<br>')
