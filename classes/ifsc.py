from lib2to3.pytree import Base
from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import json
import re
import os
from datetime import datetime
import phtml


class EventType(Enum):
    LEAD = 'lead'
    BOULDER = 'boulder'
    SPEED = 'speed'
    COMBINED = 'combined'


class Gender(Enum):
    WOMEN = 'women'
    MEN = 'men'


class Event(BaseModel):
    event: EventType
    rank: int = None

    @property
    def put(self):
        output = {
            'event': self.event.name,
            'rank': self.rank,
        }
        return output
    
    @classmethod
    def build(cls, dct):
        obj = cls(
            event=getattr(EventType, dct.get('event')),
            rank=dct.get('rank'),
        )
        return obj


class AthleteProfile(BaseModel):
    name: str
    country: str = None
    gender: Gender = None
    events: List[Event] = []

    @property
    def put(self):
        output = {
            'name': self.name,
            'country': self.country,
            'gender': self.gender.name,
            'events': [e.put for e in self.events]
        }
        return output
    
    @classmethod
    def build(cls, dct):
        obj = cls(
            name=dct.get('name'),
            country=dct.get('country'),
            gender=getattr(Gender, dct.get('gender')),
            events=[Event.build(e) for e in dct.get('events', [])]
        )
        return obj
    
    # @property
    # def html(self):
    #     element = phtml.Div()
