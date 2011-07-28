import re
import logging

from BeautifulSoup import BeautifulSoup
from scrapy.selector import XPathSelector
from exception import LoginError, CartolaError
from base import Scraper, Vault


log = logging.getLogger(__name__)


class BciScraper(Scraper):
    name = "bci"

    def __init__(self, options):

        user = options["username"]
        password = options["password"]
        self._options = options
        urls = {"login": "http://www.bci.cl/personas/",
                "cartola": "https://www.bci.cl/cuentaswls/SuperCartola",
                }
        super(BciScraper, self).__init__(urls, user, password, options)

    def login(self):
        self._browser.select_form(name="frm")
        self._browser.form.set_all_readonly(False)
        self._browser["rut"] = self._user.split("-", 1)[0]
        self._browser["dig"] = self._user.split("-", 1)[1]
        self._browser["serv"] = "SuperCartola"
        self._browser["clave"] = self._password
        self._browser["canal"] = "110"
        response = self._browser.submit()
        self.save_html(response)

        self._logged_in = True

        return response

    def get_cartola(self, html):
        dom = BeautifulSoup(html)

        return [{"account": cuenta_corriente,
                 "saldo_disponible": saldo_disponible,
                 "saldo_contable": saldo_contable,
                 }]
        dom.find('font', text=re.compile("Cuenta[ \n]+Corriente")).parent.parent.parent.parent.parent.parent.parent.nextSibling.nextSibling
        cartola_row = dom.find('font', text=re.compile("Cuenta[ \n]+Corriente")).parent.parent.parent.parent.parent.parent.parent.nextSibling.nextSibling.contents[1].contents[0].contents[1].contents[1].contents[0].contents[3]
        try:
            values = dom.find('font', text=re.compile("Cuenta[ \n]+Corriente")).parent.parent.parent.parent.parent.parent.parent.nextSibling.nextSibling.contents[1].contents[0].contents[1].contents[1].contents[0].contents[3].findAll(text=re.compile("\d+"))

            cuenta_corriente = int(values[0])
            saldo_disponible = self.parse_currency(values[1])
            saldo_contable = self.parse_currency(values[2])
        except IndexError:
            self.log.error("Cartola not found")
            raise CartolaError("Not found")

        return [{"account": cuenta_corriente,
                 "saldo_disponible": saldo_disponible,
                 "saldo_contable": saldo_contable,
                 }]


class BciVault(Vault):
    pass
