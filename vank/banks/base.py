import mechanize
import cookielib
import re

from pprint import pprint
from vank.config import settings

class Scraper(object):

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6'
    RE_CURRENCY = re.compile("^[ ]*\${1}([0-9.]+)")

    def __init__(self, urls, user, password):
        self._urls = urls
        self._user = user
        self._password = password
        self._browser = None
        self._debug = settings["DEBUG"]
        self._logged_in = False

    def setup_debug(self):

        if not self._debug:
            return

        self._browser.set_handle_equiv(True)
        self._browser.set_handle_gzip(True)
        self._browser.set_handle_redirect(True)
        self._browser.set_handle_referer(True)
        self._browser.set_handle_robots(False)

        self._browser.set_debug_http(True)
        self._browser.set_debug_redirects(True)
        self._browser.set_debug_responses(True)

    def setup(self):
        self._browser = mechanize.Browser()

        cj = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(cj)
        self._browser.addheaders = [('User-agent', self.__class__.user_agent)]

        self.setup_debug()

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

    def login(self):
        raise NotImplemented("login")

    def get_cartola(self, html):
        raise NotImplemented("get_cartola")


class Vault(object):
    pass
