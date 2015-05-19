__author__ = 'tom.pauwaert'

import json
import os, sys
from scrapy import cmdline
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
    _JSON_SET_FILE_ORIGINAL = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) \
                    + os.path.sep + "SetList.json"
    _JSON_SET_FILE_MCINFO = os.path.dirname(os.path.realpath(__file__)) \
                            + os.path.sep + "mtgset" \
                            + os.path.sep + "output" \
                            + os.path.sep + "sets_mcinfo.json"
    _SPIDER = "sets_crawler"
    _FORMAT = "json"
    _sets_original = None

    def read_sets_original(self):
        """
        Read the SetList.json file.
        Original means that the setlist information comes from mtgjson.com instead
        of a setlist that is scraped from magiccard.info
        """
        with open(self._JSON_SET_FILE_ORIGINAL) as json_file:
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


    def read_sets_mcinfo(self):
        """
        Read the set data from the magiccard.info. This data holds the codes,
        the names of the sets, and their urls on magiccard.info (relative url)
        :return:
        """
        if not os.path.isfile(self._JSON_SET_FILE_MCINFO):
            pass

    def _create_sets_mcinfo(self):
        """
        Create the mcinfo sets json file by starting the spider that crawls the set data
        from magiccard.info/sitemap.html

        TODO: Make the command line execution more robust (paths, etc....)
        :return:
        """
        print "DEBUG: Crawling http://magiccard.info/sitemap.html for set data."
        cmd =  "scrapy crawl {} -o \"{}\" -t {}".format(self._SPIDER,
                                                        "mtgset/output/sets_mcinfo.json",
                                                        self._FORMAT)
        print cmd
        os.system(cmd)
        print "DEBUG: Done crawling."

        if not os.path.isfile(self._JSON_SET_FILE_MCINFO):
            print "DEBUG: [ERROR] Crawling Unsuccesful, output file not found."



if __name__ == "__main__":
    sm = SetManager()
    # sm.read_sets_original()
    # sm.list_sets_original()
    # sm.read_sets_mcinfo()
    sm._create_sets_mcinfo()










