import os
import json

from pydantic import BaseModel
from enum import Enum
from typing import List, Union
from datetime import datetime, timedelta
from uuid import uuid4

from .utils import parse_potential_timestring


datetime_str = "%Y%m%d_%H%M%S.%fZ"


class ShorthandMapping(Enum):
    MEETING = 'CHARGE.CODE'
    WORK = 'CHARGE.CODE'
    WORKING = 'CHARGE.CODE'
    OVERHEAD = 'CHARGE.CODE'

class TimecardEntry(BaseModel):
    identifier: str = None
    update_datetime: str = None
    changelog: List[str] = []
    charge_code: str = None
    shorthand: str = None
    note: str = None
    description: str = None
    start_time: datetime = None
    end_time: datetime = None
    duration: Union[datetime, timedelta] = None
    day: datetime = None

    # Id
    @property
    def id(self):
        if self.identifier is None:
            self.identifier = str(uuid4())
        return self.identifier

    @id.setter
    def id(self, new_id):
        self.identifier = new_id

    @property
    def calculated_duration(self):
        if self.duration is not None:
            return self.duration
        return self.end_time - self.start_time

    @property
    def calculated_charge_code(self):
        code = self.charge_code
        if code is None:
            code = getattr(ShorthandMapping, self.shorthand.upper()).value
        return code

    @property
    def put(self):
        if self.update_datetime is None:
            self.update_datetime = datetime.strftime(datetime.utcnow(), datetime_str)
        content = {
            'id': self.id,
            'update_datetime': self.update_datetime,
            'changelog': self.changelog,
            'charge_code': self.charge_code,
            'shorthand': self.shorthand,
            'note': self.note,
            'description': self.description,
            'start_time': datetime.strftime(self.start_time, datetime_str) if self.start_time is not None else None,
            'end_time': datetime.strftime(self.end_time, datetime_str) if self.end_time is not None else None,
            'duration': datetime.strftime(self.duration, datetime_str) if self.duration is not None else None,
        }
        return content

    @classmethod
    def build(cls, dct):
        content = {
            'identifier': dct.get('id'),
            'update_datetime': dct.get('update_datetime'),
            'changelog': dct.get('changelog', []),
            'charge_code': dct.get('charge_code'),
            'shorthand': dct.get('shorthand'),
            'note': dct.get('note'),
            'description': dct.get('description'),
            'start_time': parse_potential_timestring(dct.get('start_time')),
            'end_time': parse_potential_timestring(dct.get('end_time')),
            'duration': parse_potential_timestring(dct.get('duration')),
        }
        obj = cls(**content)
        return obj


class Timecard:
    def __init__(self):
        self.default_file = 'data/timecard/timecard.json'
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = self.load()
        return self._data

    @data.setter
    def data(self, dct):
        self._data = dct

    def load(self, filepath=None):
        records = []
        if filepath is None:
            filepath = self.default_file
        try:
            with open(filepath, 'r') as tf:
                timecard_data = json.load(tf)
        except FileNotFoundError:
            try:
                os.makedirs('data/timecard')
            except:
                pass
            timecard_data = {}
        for item in timecard_data.get('records', []):
            item = json.loads(item)
            records.append(TimecardEntry.build(item))

        timecard_data['records'] = records

        return timecard_data

    def save(self, filepath=None, data=None):
        if filepath is None:
            filepath = self.default_file
        if data is None:
            data = self.data
        if data is None:
            return
        records = []
        for item in data.get('records', []):
            records.append(json.dumps(item.put))
        data['records'] = records
        try:
            with open(filepath, 'w') as tf:
                tf.write(json.dumps(data, indent=4))
        except FileNotFoundError:
            try:
                os.makedirs('data/timecard')
            except:
                pass
            with open(filepath, 'w') as tf:
                tf.write(json.dumps(data, indent=4))
        finally:
            self.data = None

    def add_entry(self, entry):
        data = self.data
        if 'records' not in data:
            data['records'] = []
        data['records'].append(entry)
        self.data = data


class POSTTimecardEntry(BaseModel):
    charge_code: str = None
    shorthand: str = None
    note: str = None
    description: str = None
    start_time: str = None
    end_time: str = None
    duration: str = None
    day: str = None

    def return_timecard_entry(self):
        if self.start_time is None or self.end_time is None:
            if self.duration is None:
                raise ValueError('If start and end times are not provided, a durations is required')
            if self.start_time is None and self.end_time is None:
                raise ValueError('If start and end times are both None, a day is required')
        obj = TimecardEntry(
            charge_code=self.charge_code,
            shorthand=self.shorthand,
            note=self.note,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        return obj


class PUTTimecard(BaseModel):
    records: List

    @property
    def put(self):
        content = {
            'records': self.records
        }
        return content
