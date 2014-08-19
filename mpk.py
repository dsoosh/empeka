#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib2
import json
import sys


BASE_URL = "http://pasazer.mpk.wroc.pl/position.php"


class MpkProvider(object):
    def __init__(self, lines):
        self.lines = lines

    def _prepare_request_string(self, lines):
        request_base = 'busList[bus][]={line}'
        if isinstance(lines, list):
            return '&'.join(request_base.format(line=line) for line in lines)
        elif isinstance(lines, int):
            return request_base.format(line=lines)

    def provide(self):
        response = urllib2.urlopen(BASE_URL, data=self._prepare_request_string(self.lines))
        return response.read()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Invalid arguments number. Usage:\npython mpk.py [<number>, ...]")
        sys.exit(1)
    lines = list(sys.argv[1].split(','))
    mpk = MpkProvider(lines)
    print(mpk.provide())
