__author__ = 'tom.pauwaert'

import json
import os, sys
import codecs, locale
from pprint import pprint


class SetManager(object):
    """ Class that reads the entire set json file. It gives the user
    the option to select which sets to download.

    Data members:
    - _JSON_SET_FILE
    - _sets_original: contains set list loaded from mtgjson.com

    TODO:
        1. Order sets on release date
        2. Show which sets have been downloaded already
        3. Check whether all images have been correctly identified
        4. Support multiple languages
    """
    _JSON_SET_FILE = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) \
                    + os.path.sep + "SetList.json"
    _sets_original = None

    def read_sets_original(self):
        """
        Read the SetList.json file.
        Original means that the setlist information comes from mtgjson.com instead
        of a setlist that is scraped from magiccard.info
        """
        with open(self._JSON_SET_FILE) as json_file:
            self._sets_original = json.load(json_file)

    def list_sets_original(self):
        """
        List the original data sets: print with an id number.
        Requires read_sets_original to be called first to populate the list.
        :return:
        """
        visual_counter = 1
        for set in self._sets_original:
            cleaned_name = set['name'].encode("ascii", 'replace')
            print("{} - {} (released on: {})".format(visual_counter, cleaned_name, set['releaseDate']))
            visual_counter += 1


if __name__ == "__main__":
    sm = SetManager()
    sm.read_sets_original()
    sm.list_sets_original()
