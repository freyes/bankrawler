import sys
import os
import os.path
import logging
import logging.config

import banks.bci

from config import settings
from optparse import OptionParser


log = None

def setup_options(args=None):

    if not args:
        args = sys.argv[1:]

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    parser.add_option("-s", "--save",
                      dest="save_directory",
                      help="Save the HTML files to DIR",
                      metavar="DIR",
                      default=None)

    (options, args) = parser.parse_args(args)

    return options


def setup_logging(options, settings):
    import data

    logconfig = os.path.join(os.path.dirname(os.path.abspath(data.__file__)),
                             "logging.conf")
    logging.config.fileConfig(logconfig)

    # if settings["loglevel"] != None:
    #     logging.getLogger().setLevel(getattr(logging,
    #                                          settings["loglevel"]))


def main():
    global log

    options = setup_options()

    setup_logging(options, settings)
    log = logging.getLogger(__name__)

    if options.save_directory:
        if not os.path.isdir(options.save_directory):
            os.makedirs(options.save_directory)

    # TODO: make this dynamic
    bank_scrapers_map = {"bci": banks.bci.BciScraper}

    for bank in settings["banks"].keys():
        klass = bank_scrapers_map[bank]

        scraper_options = {}
        settings.interpolation = False
        scraper_options["filename_format"] = settings["filename_format"]
        settings.interpolation = True
        scraper_options["save_directory"] = options.save_directory
        scraper_options["debug"] = True
        scraper_options.update(settings["banks"][bank])

        scraper = klass(scraper_options)
        scraper.run()

if __name__ == '__main__':
    main()
