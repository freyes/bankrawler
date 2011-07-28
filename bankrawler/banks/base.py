import os.path
import mechanize
import cookielib
import re
import hashlib
import datetime
import logging
import base64
from pprint import pprint
from decorators import Property
from exception import LoginError


log = logging.getLogger(__name__)


DEFAULT_UA = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6'


class Browser(mechanize.Browser):

    user_agent = DEFAULT_UA

    def __init__(self, *args, **kwargs):

        _debug = kwargs.pop("debug", False)
        self.use_cache = kwargs.pop("use_cache", False)

        mechanize.Browser.__init__(self, *args, **kwargs)

        cj = cookielib.LWPCookieJar()
        self.set_cookiejar(cj)
        self.addheaders = [('User-agent', self.__class__.user_agent)]
        self.set_handle_equiv(True)
        self.set_handle_gzip(True)
        self.set_handle_redirect(True)
        self.set_handle_referer(True)
        self.set_handle_robots(False)

        self.debug = _debug

    def open(self, *args, **kwargs):
        if self.use_cache:
            # TODO: read the cached file(s)
            pass
        else:
            return mechanize.Browser.open(self, *args, **kwargs)

    # properties
    @Property
    def debug ():
        doc = "enable debug"

        def fget (self):
            return self._debug

        def fset (self, value):

            self.set_debug_http(value)
            self.set_debug_redirects(value)
            self.set_debug_responses(value)
            self._debug = value

        def fdel (self):
            del self._debug



class Scraper(object):

    RE_CURRENCY = re.compile("^[ ]*\${1}([0-9.]+)")

    def __init__(self, urls, user, password, options={}):
        self._user_agent = options.get("user_agent", DEFAULT_UA)
        self._urls = urls
        self._user = user
        self._password = password
        self._browser = None
        self._debug = options.get("debug", False)
        self._logged_in = False
        self._options = options


    def setup(self):
        self._browser = Browser(debug=self._debug)

    def run(self):

        self.setup()

        # login
        self._browser.open(self._urls["login"])
        assert self._browser.viewing_html()
        response = self.login()

        if response == None or not self._logged_in:
            raise LoginError()

        # get the cartola
        html = self._browser.open(self._urls["cartola"])
        assert self._browser.viewing_html()
        self.save_html(html)

        # scrape it!
        self._cartola = self.get_cartola(html)

        pprint(self._cartola)

    def parse_currency(self, value):
        currency_re = self.__class__.RE_CURRENCY

        matched = currency_re.match(value)

        if matched:
            return int(matched.group(1).replace(".", ""))
        else:
            return value

    def save_html(self, response):

        if self._options["save_directory"] and response != None:
            fname = os.path.join(self._options["save_directory"],
                                 self._build_name())
            log.debug("Saving response to %s" % fname)
            output = open(fname, "w")
            output.write(response.read())
            output.close()

    def _build_name(self):

        url = self._browser.geturl()
        url_base64 = base64.b64encode(url)

        return self._options["filename_format"] % {"bank": self.__class__.name,
                                                   "asctime": datetime.datetime.now().isoformat(),
                                                   "url_base64": url_base64,
                                                   "url": url}

    def login(self):
        raise NotImplemented("login")

    def get_cartola(self, html):
        raise NotImplemented("get_cartola")


class Vault(object):
    pass
