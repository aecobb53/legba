import os
import json

from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4


datetime_str = "%Y%m%d_%H%M%S.%fZ"


class TimecardEntry(BaseModel):
    _id: str = None
    update_datetime: str = None
    changelog: List[str] = []
    charge_code: str = None
    shorthand: str = None
    note: str = None
    description: str = None
    start_time: str = None
    end_time: str = None

    # Id
    @property
    def id(self):
        if self._id is None:
            self._id = str(uuid4())
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

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
            'start_time': self.start_time,
            'end_time': self.end_time,
        }
        return content

    @classmethod
    def build(cls, dct):
        content = {
            'datetime': dct['datetime']
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

    def add_entry(self, entry):
        data = self.data
        if 'records' not in data:
            data['records'] = []
        data['records'].append(entry)
        self.data = data


class POSTTimecardEntry(BaseModel):
    charge_code: str = None
    note: str = None
    description: str = None
    start_time: str = None
    end_time: str = None

    def return_timecard_entry(self):
        obj = TimecardEntry()
        return obj


