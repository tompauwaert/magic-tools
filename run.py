__author__ = 'tom.pauwaert'
from gatherer.set_downloader import SetManager, download_sets

sm = SetManager()
# sm.read_sets_original()
sm.list_sets_original()
# sm.read_sets_mcinfo()
# sm.read_sets_mcinfo()
# sm._create_sets_original()

print "Which sets do you wish to download? Provide a comma separated list."
sets = map(str.strip, raw_input().split(","))
download_sets(sets, sm)
