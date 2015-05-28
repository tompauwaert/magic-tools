import json
import os
import inspect
import os.path
from collections import OrderedDict
from scrapy.settings import Settings
from pprint import pprint
from crawler import run_crawler
from gatherer.mtgset.spiders.setlist_spider import SetListSpider


class SetManager(object):
    """ Class that reads the entire set json file. It gives the user
    the option to select which sets to download.

    Private Data members [constant]:
    - _JSON_SET_FILE_ORIGIINAL = Sets and codes based on the 'AllSets.Json' document
    - _JSON_SET_FILE_MCINFO = Set names, codes and magiccards.info urls for the sets
    - _JSON_ALL_SETS = The file containing all set and card information
    - _SPIDER = Spider name to scrape magiccards.info set information
    - _FORMAT = Format used to save the scraped data in.

    Private Data members:
    - _sets_original: contains set list loaded from mtgjson.com (read from file)
    - _sets_mcinfo: set information (read from file) from magiccards.info

    Public Data members:
    - CODE: identifier for normal set codes
    - OLDCODE: identifier for old set codes - compatibility with certain software
    - GCODE: identifier for set codes on gatherer.wizards.com - if it differs from CODE
    - MCICode; set code used by magiccards.info - if the set exists on magiccards.info

    TODO:
        2. Show which sets have been downloaded already
        3. Check whether all images have been correctly identified
        4. Support multiple languages
    """
    _JSON_SET_FILE_ORIGINAL = (os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
                               + os.path.sep + "mtgset"
                               + os.path.sep + "output"
                               + os.path.sep + "SetList.json")
    _JSON_ALL_SETS = (os.path.dirname(os.path.realpath(__file__))
                      + os.path.sep + "AllSets-x.json")
    _JSON_SET_FILE_MCINFO = (os.path.dirname(os.path.realpath(__file__))
                             + os.path.sep + "mtgset"
                             + os.path.sep + "output"
                             + os.path.sep + "sets_mcinfo.json")
    _JSON_SET_FILE_MCINF_URI = "file:///D:/dev/python/magic-tools/gatherer/mtgset/output/sets_mcinfo.json"
    _SPIDER = "setlist-spider"
    _FORMAT = "json"

    CODE = "code"
    OLDCODE = "oldcode"
    GCODE = "gathererCode"
    MCICODE = "magicCardsInfoCode"

    def __init__(self):
        """
        Initialize the
        :return:
        """
        self._sets_original = None
        self._sets_mcinfo = None

    def map_code(self, code, original_ct=None, to_ct=None):
        """
        Map a code from one version to another.\n

        :param code: code we try to map.\n
        :param original_ct: origin of the original_ct code\n
        :param to_ct: format we wish to map the code to.\n
        :return: the corresponding code in the destination format. Or None if the code
            had no special mapping in the destination format.\n
        :raises ValueError: - if the 'code' is a non-existing code.\n
                            - if 'original_ct' or 'to_ct' are non existing code identifiers
                              (e.g. CODE, OLDCODE, GCODE, MCICODE)\n
        """
        if original_ct is None:
            original_ct = self.CODE
        if to_ct is None:
            to_ct = self.MCICODE
        if self._sets_original is None:
            self.read_sets_original()

        codes = [self.CODE, self.OLDCODE, self.GCODE, self.MCICODE]
        if original_ct not in codes:
            raise ValueError("Invalid _original_ code: '{}'".format(original_ct))
        if to_ct not in codes:
            raise ValueError("Invalid _to_ code: '{}'".format(to_ct))

        for key in self._sets_original:
            if (original_ct in self._sets_original[key].keys() and
                    self._sets_original[key][original_ct] == code):
                if to_ct in self._sets_original[key].keys():
                    return self._sets_original[key][to_ct]
                else:
                    return None

        raise ValueError("Code '{}' does not exist".format(code))

    def get_mci_set_info(self, code):
        """
        Get the magiccards.info information for a default set.\n
        :param code: code of the set - this is magiccards.info code name of the set.\n
        :return: This returns the following set information in a dictionary.\n
        - "name" : magiccards.info name of the set.\n
        - "url" : magiccards.info url to the set\n
        - "code" : magiccards.info code of the set\n
        If the code is not recognized, this method returns None.\n
        """
        if self._sets_mcinfo is None:
            self.read_sets_mcinfo()

        for key in self._sets_mcinfo:
            if self._sets_mcinfo[key]['code'] == code:
                return self._sets_mcinfo[key]

        return None

    def read_sets_original(self):
        """
        Read the SetList.json file.\n
        Original means that the setlist information comes from mtgjson.com instead
        of a setlist that is scraped from magiccard.info\n
        """
        if not os.path.isfile(self._JSON_SET_FILE_ORIGINAL):
            self._create_sets_original()

        with open(self._JSON_SET_FILE_ORIGINAL) as json_file:
            self._sets_original = json.load(json_file, encoding='utf-8')

    def list_sets_original(self):
        """
        List the original data sets: print with an id number.
        Requires read_sets_original to be called first to populate the list.\n
        Side-effect: The original set data will be sorted on release date in ascending order.\n
        :return:
        """
        if self._sets_original is None:
            self.read_sets_original()

        sorted_list = sorted(self._sets_original.items(),
                             cmp=lambda x, y: cmp(x[1]["releaseDate"], y[1]["releaseDate"])
                             )
        self._sets_original = OrderedDict()
        for (key, value) in sorted_list:
            self._sets_original[key] = value

        for key in self._sets_original:
            cleaned_name = self._sets_original[key]["name"].encode("ascii", "replace")
            print("{: <10} - {} (released on: {})".format(
                key,
                cleaned_name,
                self._sets_original[key]['releaseDate']
            ))

    def read_sets_mcinfo(self):
        """
        Read the set data from the magiccard.info. This data holds the codes,
        the names of the sets, and their urls on magiccard.info (relative url)
        :return:
        """
        if not os.path.isfile(self._JSON_SET_FILE_MCINFO):
            self._create_sets_mcinfo()

        with open(self._JSON_SET_FILE_MCINFO) as json_file:
            self._sets_mcinfo = json.load(json_file, encoding='utf-8')

    def _create_sets_mcinfo(self):
        """
        Create the mcinfo sets json file by starting the spider that crawls the set data
        from magiccard.info/sitemap.html\n
        \n
        TODO: Make the command line execution more robust (paths, etc....)
        :return:
        """
        print "DEBUG: Crawling http://magiccard.info/sitemap.html for set data."
        # cmd = "scrapy crawl {} -o \"{}\" -t {}".format(
        #     self._SPIDER,
        #     "mtgset/output/sets_mcinfo.json",
        #     self._FORMAT
        # )
        # print cmd
        # os.system(cmd)

        settings = {
            'FEED_URI' : self._JSON_SET_FILE_MCINF_URI,
            'FEED_FORMAT' : 'json',
        }
        spider = SetListSpider()
        # location =  inspect.getfile(spider.__class__)
        # location = os.path.splitext(location)[0] + os.extsep + "py"
        location = 'mtgset/spiders/setlist_spider.py'
        run_crawler(location, [], settings)

        # with open(self._JSON_SET_FILE_MCINFO, 'w') as file:
        #     json.dump(results, file)

        print "DEBUG: Done crawling."

        if not os.path.isfile(self._JSON_SET_FILE_MCINFO):
            print "DEBUG: [ERROR] Crawling Unsuccesful, output file not found."

    def _create_sets_original(self):
        """
        Create a list of all sets in json format. The list contains following fields for each set:\n
        - name\n
        - releaseDate\n
        - code\n
        - gathererCode\n
        - oldCode\n
        - magicCardsInfoCode\n
        \n
        This data can be used to map magiccardsinfo data scraped from their website to their
        set counterparts using the official codes.\n
        :return:
        """
        with open(self._JSON_ALL_SETS) as json_file:
            _all_sets = json.load(json_file, encoding='utf-8')
            _set_list = {}

            for key in _all_sets.keys():
                _set_list[key] = {}
                _set_list[key]['name'] = _all_sets[key]['name']
                _set_list[key]['releaseDate'] = _all_sets[key]['releaseDate']
                _set_list[key][self.CODE] = _all_sets[key][self.CODE]

                if self.GCODE in _all_sets[key].keys():
                    _set_list[key][self.GCODE] = _all_sets[key][self.GCODE]

                if self.OLDCODE in _all_sets[key].keys():
                    _set_list[key][self.OLDCODE] = _all_sets[key][self.OLDCODE]

                if self.MCICODE in _all_sets[key].keys():
                    _set_list[key][self.MCICODE] = _all_sets[key][self.MCICODE]

        with open(self._JSON_SET_FILE_ORIGINAL, 'w') as output:
            json.dump(_set_list, output, indent=4)
            print "I'm here!"


if __name__ == "__main__":
    sm = SetManager()
    # sm.read_sets_original()
    sm.list_sets_original()
    # sm.read_sets_mcinfo()
    # sm.read_sets_mcinfo()
    # sm._create_sets_original()

