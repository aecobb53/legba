from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import json
import re
import os
from datetime import datetime,  timedelta
import phtml

from .mosaic import Mosaic#, IFSCMosaic, TrafficMosaic


class Wall:
    def __init__(self, mosaics = [], color_scheme={}):
        self.mosaics = mosaics
        self.date = None
        self.last_updated = None
        self.color_scheme = color_scheme # Add a default color scheme

        self.doc = phtml.Document()

    @property
    def put(self):
        output = {}
        return output

    @property
    def html(self):
        # doc = phtml.Document()
        # mosaic_content = []
        for mosaic in self.mosaics:
            # mosaic_content.append(mosaic.html)
            self.doc.body.append(mosaic.html)
            self.doc.body.append(phtml.LineBreak())
        # a = phtml.LineBreak()
        # b = phtml.LineBreak().return_content
        # c = f"{phtml.LineBreak().return_content}"
        # d = "".join(mosaic_content)
        # e = f"".join(mosaic_content)
        # f = f"{phtml.LineBreak().return_content}".join(mosaic_content)
        # x=1
        # self.doc.body.append(f"{phtml.LineBreak().return_content}".join(mosaic_content))
        return self.doc.return_document

    @classmethod
    def build(cls, dct):
        obj = cls()
        return obj

    def add_mosaic(self, mosaic):
        self.mosaics.append(mosaic)
