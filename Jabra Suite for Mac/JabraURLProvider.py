#!/usr/bin/python
#
# Copyright 2018 soberhofer
# Based on the BareBonesURLProvider by Tim Sutton (https://github.com/autopkg/recipes/blob/master/Barebones/BarebonesURLProvider.py)
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
# suppress 'missing class member env'
#pylint: disable=e1101

import urllib2
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError

__all__ = ["JabraURLProvider"]

class JabraURLProvider(Processor):
    """Provides a version and dmg download for Jabra Suite for Mac."""
    description = __doc__
    input_variables = {
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
        try:
            tree = ET.ElementTree(file=urllib2.urlopen("https://www.jabra.com/macsuite/JMSVersionUpdate.xml"))
            root = tree.getroot()
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
