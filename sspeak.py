#!/usr/bin/env python
#
# Copyright 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Tails a realtime search using the export endpoint and prints results to
   stdout."""

import sys, subprocess, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pprint import pprint

from splunklib.client import connect
from splunklib.results import ResultsReader

try:
    import utils
except ImportError:
    raise Exception("Add the SDK repository to your PYTHONPATH to run the examples "
                    "(e.g., export PYTHONPATH=~/splunk-sdk-python.")

def main():
    usage = "usage: %prog <search>"
    opts = utils.parse(sys.argv[:], {}, ".splunkrc", usage=usage)

    if len(opts.args) != 2:
        utils.error("filter mode and search expression required", 2)
    search = opts.args[1]
    fmode = opts.args[0]
    
    service = connect(**opts.kwargs)

    try:
        result = service.get(
            "search/jobs/export",
            search=search,
            earliest_time="rt", 
            latest_time="rt", 
            search_mode="realtime")

        for result in ResultsReader(result.body):
            if result is not None:
                if isinstance(result, dict):
                        event=result.items()[2][1]
                        shorte=event[61:]
                        if fmode == '-ao':
                            valids = re.sub(r"[^A-Za-z ]+", '', shorte)
                            print valids
                            subprocess.call(["/usr/bin/say", valids])
                        elif fmode == '-an':
                            print shorte
                            subprocess.call(["/usr/bin/say", shorte])
    except KeyboardInterrupt:
        print "\nInterrupted."

if __name__ == "__main__":
    main()

