# Copyright (C) 2011 Felipe Reyes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path

from setuptools import setup, find_packes()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name = "bankdat",
      version = "0.1",
      author = "Felipe Reyes",
      author_email = "freyes@tty.cl",
      description = "A simple tool to gather the data of your bank account",
      license = "GPLv3",
      keywords = "bank report tool",
      url = "http://tty.cl/bankdat",
      packages=find_packes(),
      long_description=read('README'),
      zip_safe = False,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 2.5"
        ],
      )
