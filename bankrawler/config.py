import sys
import os
import os.path
import validate
import logging

from configobj import ConfigObj, ConfigObjError

log = logging.getLogger(__name__)


class Configuration(ConfigObj):
    def __init__(self):

        self._fspec = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "data",
                                   "config.spec")

        _filename = os.path.join(os.environ["HOME"], ".config",
                                 "bankrawler", "bankrawler")
        if not os.path.isfile(_filename):
            f = open(_filename, "w")
            f.close()

        try:
            super(Configuration, self).__init__(infile=_filename)
        except ConfigObjError, ex:
            log.error(ex.errors)

            for err in ex.errors:
                sys.stderr.write("%s\n" % err)

            raise SystemExit

        # TODO: write the config spec
        # validator = validate.Validator()
        # self.validate(validator)


class Validator(validate.Validator):
    def __init__(self):
        super(Validator, self).__init__()

    def read_spec(self):
        return open(self._fspec).read()


settings = Configuration()
