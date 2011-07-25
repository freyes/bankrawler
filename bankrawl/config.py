import os
import os.path
import validate

from configobj import ConfigObj


class Configuration(ConfigObj):
    def __init__(self):

        self._fspec = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "data",
                                   "config.spec")

        _filename = os.path.join(os.environ["HOME"], ".config", "bankdat")
        if not os.path.isfile(_filename):
            f = open(_filename, "w")
            f.close()

        super(Configuration, self).__init__(infile=_filename,
                                            configspec=self._fspec)

        # TODO: write the config spec
        # validator = validate.Validator()
        # self.validate(validator)


class Validator(validate.Validator):
    def __init__(self):
        super(Validator, self).__init__()

    def read_spec(self):
        return open(self._fspec).read()


settings = Configuration()
