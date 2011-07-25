import sys
import pdb
import code

from config import settings
from banks import bci


DEBUG=settings["DEBUG"]


if __name__ == '__main__':

    bank = sys.argv[1]

    scraper = bci.BciScraper(settings[bank])
    scraper.run()
