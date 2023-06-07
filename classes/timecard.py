import json

from pydantic import BaseModel
from datetime import datetime


datetime_str = "%Y%m%d_%H%M%S.%fZ"


class TimecardEntry(BaseModel):
    datetime: str = None

    @property
    def put(self):
        if self.datetime is None:
            self.datetime = datetime.strftime(datetime.utcnow(), datetime_str)
        content = {
            'datetime': self.datetime,
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
        except Exception as err:
            print(err)
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


