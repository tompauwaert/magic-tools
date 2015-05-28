from gatherer.crawler import CrawlerWorker
from gatherer.set_manager import SetManager
from gatherer.mtgset.utility import is_sequence
from multiprocessing import freeze_support


def download_sets(codes, set_manager=None):
    """
    Download an mtg set from magiccards.info. \n
    :param code: codes of the set to download. The official code is expected here. The
    expected parameter is a list.\n
    :param set_manager the set manager to be used for the downloading. This parameter
    is optional. If no setmanager is given, a new one is created.\n
    :return: None
    """
    if not is_sequence(codes):
        raise ValueError("Expecting iterable list of codes. Argument is of type: {}".format(
            type(codes)
        ))

    from gatherer.mtgset.spiders.set_spider import SetSpider
    # TODO: Check that each set in codes is an existing code.
    # cmd = "scrapy crawl set-spider code_list={} -o test.json -t json".format(",".join(codes))
    results = []
    # crawler = CrawlerWorker(SetSpider(code_list=codes))



def run():
    sm = SetManager()
    # sm.read_sets_original()
    # sm.list_sets_original()
    # sm.read_sets_mcinfo()
    # sm.read_sets_mcinfo()
    # sm._create_sets_original()
    sm._create_sets_mcinfo()

    # print "Which sets do you wish to download? Provide a comma separated list."
    # sets = map(str.strip, raw_input().split(","))
    # download_sets(sets, sm)

if __name__ == "__main__":
    freeze_support()
    run()
