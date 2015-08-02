import os
import json
import sys


class SiteConfig:

    def __init__(self):
        self.data = {}

        if SiteConfig.deploy_is_production():
            self.load('./prod.json')
            print("Loading config_data file: ./prod.json")
        else:
            self.load('./dev.json')
            print("Loading config_data file: ./dev.json")

        self.cache_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), self.get_val("cache_folder"))
        )
        self.download_base_url = self.get_val("download_base_url")

    @staticmethod
    def deploy_is_production():
        is_prod = 'uwsgi' in sys.argv
        return is_prod

    def load(self, config_file):
        full_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), config_file)
        )

        with open(full_file) as fin:
            self.data = json.load(fin)

    def get_val(self, key):
        return self.data[key]
