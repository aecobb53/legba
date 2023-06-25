from ast import parse
import os
import json
from unittest.mock import NonCallableMagicMock

from pydantic import BaseModel
from enum import Enum
from typing import List, Union
from datetime import datetime, timedelta
from uuid import uuid4

from .utils import parse_potential_timestring


datetime_str = "%Y%m%dT%H%M%S.%fZ"
date_str = "%Y%m%dZ"


class ShorthandMapping(Enum):
    MEETING = 'CHARGE.CODE.1'
    WORK = 'CHARGE.CODE.2'
    WORKING = 'CHARGE.CODE.2'
    OVERHEAD = 'CHARGE.CODE.3'
    GENERAL = 'GENERAL'


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
    def day_str(self):
        return datetime.strftime(self.day, date_str)

    @property
    def put(self):
        if self.update_datetime is None:
            self.update_datetime = datetime.strftime(datetime.utcnow(), datetime_str)
        duration = None
        if self.duration:
            hrs, rem = divmod(self.duration.seconds, 3600)
            mins, rem = divmod(rem, 60)
            secs, rem = divmod(rem, 60)
            duration = f"{hrs}:{mins}:{secs}"
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
            'duration': duration,
            'day': datetime.strftime(self.end_time, date_str)
        }
        return content

    @classmethod
    def build(cls, dct):
        duration = None
        if dct.get('duration'):
            print(dct['duration'])
            try:
                hours, minutes, seconds = dct['duration'].split(':')
                duration = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            except Exception as err:
                print(err)
                duration = timedelta(float(dct['duration']))
        print(f"DAY:::: {dct.get('day')}")
        day = parse_potential_timestring(dct.get('day'))
        if not day:
            if dct.get('start_time'):
                day = parse_potential_timestring(dct['start_time'])
            else:
                day = parse_potential_timestring(dct['end_time'])
        print(f"DAY:   {day}")
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
            # 'duration': parse_potential_timestring(dct.get('duration')),
            'duration': duration,
            'day': day,
        }
        obj = cls(**content)
        return obj


class DayOfEntries(BaseModel):
    day: datetime
    records: List[TimecardEntry] = []

    @property
    def day_str(self):
        return datetime.strftime(self.day, date_str)

    @property
    def day_array_value(self):
        value = self.day.year * 10_000
        value += self.day.month * 100
        value += self.day.day
        return value

    @property
    def put(self):
        content = {
            'day': self.day,
            'records': self.day_str,
        }
        return content

    @classmethod
    def build(cls, dct):
        content = {}
        obj = cls(**content)
        return obj

    @classmethod
    def calculate_duration_value(cls, datetime_obj):
        hours, rem = divmod(datetime_obj.seconds, 3600)
        minutes, rem = divmod(rem, 60)
        minutes = int(minutes / 15) * .25
        return hours + minutes

    def calculate_details(self):
        codes = {}
        """
        I need to find a way to track records that only have a start and an end time without grabing ones that have either with a duration and not counting them twice
        """
        for record in self.records:
            charge_code = None
            duration = None
            if record.charge_code:
                charge_code = record.charge_code
            elif record.shorthand:
                try:
                    charge_code = getattr(ShorthandMapping, record.shorthand.upper()).value
                except:
                    charge_code = 'UNKNOWN'
            if record.duration:
                duration = record.duration
            elif record.end_time and record.start_time:
                duration = record.end_time - record.start_time
            elif record.end_time and not record.start_time:
                x=1
                pass
                # for record 

            if charge_code not in codes:
                codes[charge_code] = 0
            if duration is None:
                continue
            codes[charge_code] += DayOfEntries.calculate_duration_value(duration)
        x=1
        if ShorthandMapping.GENERAL.value in codes:
            try:
                work_value = codes[ShorthandMapping.GENERAL.value] - codes[ShorthandMapping.MEETING.value]
            except:
                work_value = 0
            if ShorthandMapping.WORK.value not in codes:
                codes[ShorthandMapping.WORK.value] = 0
            codes[ShorthandMapping.WORK.value] += work_value
            del codes[ShorthandMapping.GENERAL.value]
        return codes


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
        print('laoding record')
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
        print(f"TIMECARD_DATA: {timecard_data}")
        for item in timecard_data.get('records', []):
            print(f"ITEM1: {item}")
            item = json.loads(item)
            print(f"ITEM2: {item}")
            records.append(TimecardEntry.build(item))

        timecard_data['records'] = records

        return timecard_data

    def save(self, filepath=None, data=None):
        print('starting save')
        if filepath is None:
            filepath = self.default_file
        if data is None:
            data = self.data
        if data is None:
            return
        records = []
        for item in data.get('records', []):
            print(f"ITEM: {item}")
            records.append(json.dumps(item.put))
        data['records'] = records
        print(f"RECORDS: {data['records']}")
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

    def display_data(self):
        tracking = {}
        data = self.data
        print('display data is being run')
        print(data)
        for record in data['records']:
            x=1
            print(f"Record: {record}")
            if record.day_str not in tracking:
                tracking[record.day_str] = DayOfEntries(day=record.day)
            tracking[record.day_str].records.append(record)
        keys_list = list(tracking.keys())
        keys_list.sort()
        print(keys_list)
        ordered_tracking = {k: tracking[k] for k in keys_list}
        output = {}
        for day, day_obj in ordered_tracking.items():
            output[day] = day_obj.calculate_details()
        return output


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

        # print(f"charge_code: {self.charge_code}")
        # print(f"shorthand: {self.shorthand}")
        # print(f"note: {self.note}")
        # print(f"description: {self.description}")
        # print(f"start_time: {self.start_time}")
        # print(f"end_time: {self.end_time}")
        # print(f"duration: {self.duration}")
        # print(f"day: {self.day}")

        if self.start_time is None and self.end_time is None and self.day is None:
            raise ValueError('If start and end times are both None, a day is required')

        # if self.start_time is None or self.end_time is None:
        #     if self.duration is None:
        #         raise ValueError('If start and end times are not provided, a durations is required')
        #     if self.start_time is None and self.end_time is None and self.day is None:
        #         raise ValueError('If start and end times are both None, a day is required')
        content = {
            'charge_code': self.charge_code,
            'shorthand': self.shorthand,
            'note': self.note,
            'description': self.description,
            # 'start_time': self.start_time,
            # 'end_time': self.end_time,
        }
        if self.start_time is not None:
            content['start_time'] = parse_potential_timestring(self.start_time)

        if self.end_time is not None:
            content['end_time'] = parse_potential_timestring(self.end_time)

        if self.duration is not None:
            # content['duration'] = parse_potential_timestring(self.duration)
            content['duration'] = timedelta(hours=float(self.duration))

        if self.day is not None:
            content['day'] = parse_potential_timestring(self.day)

        # print(content)

        obj = TimecardEntry(**content)
        return obj


class PUTTimecard(BaseModel):
    records: List

    @property
    def put(self):
        content = {
            'records': self.records
        }
        return content
