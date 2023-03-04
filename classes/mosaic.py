from lib2to3.pytree import Base
from turtle import back
from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import json
import re
import os
from datetime import datetime
import phtml

from tile import TargetElement, LinkElement, Tile


class Mosaic(BaseModel):
    # date = None
    # last_updated = None

    # date = None
    last_updated: datetime = datetime.now()
    title: str = None

    tiles: List[Tile] = []

    classes: List[str] = ['mosaic']

    @property
    def put(self):
        output = {
            'title': self.title,
            'last_updated': datetime.strftime(self.last_updated, '%Y-%m-%dT%H:%M:%SZ'),
            'tiles': [t.put for t in self.tiles],
        }
        return output

    @property
    def datetime_format(self):
        # return "%Y"
        return "%Y-%m-%dT%H:%M:%SZ"

    @property
    def html(self):
        div = phtml.Div()
        for css_class in self.classes:
            div.add_class(css_class)
        div.add_internal(phtml.Header(level=1, internal=self.title))
        for tile in self.tiles:
            div.internal.append(tile.html)
        return div

        """
        
        # div.add_internal(phtml.Header(
        #     level=3,
        #     internal=f"Last updated: {datetime.strftime(self.last_updated, self.datetime_format)}")
        # )
        for tile in self.tiles:
            div.internal.append(tile.html)
        return div
        """

    @classmethod
    def build(cls, dct):
        obj = cls(
            title=dct.get('title'),
            last_updated=datetime.strptime(dct.get('last_updated'), '%Y-%m-%dT%H:%M:%SZ'),
            tiles=[Tile.build(t) for t in dct.get('tiles', [])]
        )
        return obj

    def add_tile(self, tile):
        self.tiles.append(tile)


class TrafficMosaic(Mosaic):
    # date = None

    title = 'Traffic Notices:'

    @property
    def put(self):
        pass

    @property
    def html(self):
        div = super().html
        div.add_class('traffic')
        div.add_internal(phtml.Header(level=1, internal=self.title))
        # div.add_internal(phtml.Header(
        #     level=3,
        #     internal=f"Last updated: {datetime.strftime(self.last_updated, self.datetime_format)}")
        # )
        for tile in self.tiles:
            div.internal.append(tile.html)
        return div

    @classmethod
    def build(cls, dct):
        obj = cls()
        return obj


class IFSCMosaic(Mosaic):
    # date = None

    title = 'IFSC Standings and Updates:'

    @property
    def put(self):
        output = super().put
        output['title'] = self.title
        return output

    @property
    def html(self):
        div = super().html
        div.add_class('mosaic-ifsc')
        div.add_internal(phtml.Header(level=1, internal=self.title))
        # div.add_internal(phtml.Header(
        #     level=3,
        #     internal=f"Last updated: {datetime.strftime(self.last_updated, self.datetime_format)}")
        # )
        for tile in self.tiles:
            div.internal.append(tile.html)
        return div

    @classmethod
    def build(cls, dct):
        obj = cls(
            title=dct.get('title'),
            last_updated=dct.get('last_updated'),
            tiles=[Tile.build(t) for t in dct.get('tiles', [])]
        )
        return obj
