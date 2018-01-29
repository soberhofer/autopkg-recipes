#!/usr/bin/python
#
# Copyright 2013 Timothy Sutton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for BarebonesURLProvider class"""
# suppress 'missing class member env'
#pylint: disable=e1101

import urllib2
import plistlib
from distutils.version import LooseVersion
from operator import itemgetter
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError

__all__ = ["JabraURLProvider"]

import ssl
from functools import wraps
def sslwrap(func):
    """http://stackoverflow.com/a/24175862"""
    @wraps(func)
    def wraps_sslwrap(*args, **kw):
        """Monkey-patch for sslwrap to force TLSv1"""
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return wraps_sslwrap

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

class JabraURLProvider(Processor):
    """Provides a version and dmg download for the Barebones product given."""
    description = __doc__
    input_variables = {
        "product_name": {
            "required": True,
            "description":
                "Product to fetch URL for. One of 'textwrangler', 'bbedit'.",
        },
    }
    output_variables = {
        "version": {
            "description": "Version of the product.",
        },
        "url": {
            "description": "Download URL.",
        }
    }

    def main(self):
        '''Find the download URL'''
        def compare_version(this, that):
            '''compare LooseVersions'''
            return cmp(LooseVersion(this), LooseVersion(that))
            
        prod = "jabra"
        url = "https://www.jabra.com/macsuite/JMSVersionUpdate.xml"
        try:
            manifest_str = urllib2.urlopen(url).read()
        except BaseException as err:
            raise ProcessorError(
                "Unexpected error retrieving product manifest: '%s'" % err)

        try:
            tree = ET.ElementTree(file=urllib2.urlopen(url))
            root = tree.getroot()
            root.tag, root.attrib
            
            version = root[1].text
            url = root[4].text
        except BaseException as err:
            raise ProcessorError(
                "Unexpected error parsing manifest as a xml: '%s'" % err)

        self.env["version"] = version
        self.env["url"] = url
        self.output("Found URL %s" % self.env["url"])

if __name__ == "__main__":
    PROCESSOR = JabraURLProvider()
    PROCESSOR.execute_shell()
