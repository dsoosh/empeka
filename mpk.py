#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import webbrowser
from argparse import ArgumentParser
import json

import requests


class Vehicle(object):
    def __init__(self, **data):
        self._id = data.pop('k')
        self._x = data.pop('x')
        self._y = data.pop('y')
        self._line = data.pop('name')

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def line(self):
        return self._line

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def update(self, other):
        self._x = other._x
        self._y = other._y


class Bus(Vehicle):
    pass


class Tram(Vehicle):
    pass


def _add_vehicle_marker(map_url, vehicle):
    map_url += '&markers=label:{line}|{x},{y}'.format(line=vehicle.line, x=vehicle.x, y=vehicle.y)
    return map_url


def _prepare_request_string(lines):
    request_base = 'busList[][]={line}'
    if isinstance(lines, list):
        return '&'.join(request_base.format(line=line) for line in lines)
    elif isinstance(lines, int):
        return request_base.format(line=lines)


def _convert(vehicles):
    vs = []
    for vehicle in vehicles:
        _type = vehicle.pop('type')
        vs.append({'bus': Bus, 'tram': Tram}.get(_type)(**vehicle))
    return vs


def get(lines):
    response = requests.post("http://pasazer.mpk.wroc.pl/position.php", data=_prepare_request_string(lines),
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if response.status_code == 200:
        return _convert(json.loads(response.content))
    return []


def show(lines):
    vehicles = get(lines)
    map_url = "http://maps.google.com/maps/api/staticmap?center=Wroclaw,Polska&zoom=12&size=1000x1000"
    for vehicle in vehicles:
        map_url = _add_vehicle_marker(map_url, vehicle)
    webbrowser.open(map_url)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('line', nargs='+', help='Line number')
    parser.add_argument('--map', '-m', action='store_true', help="Show on google maps (static)")
    args = parser.parse_args()
    if args.map:
        show(args.line)
