from importlib.metadata import entry_points
from sqlite3 import Time
from time import time
from turtle import pos
from unittest import result
import pytest
import json
from classes.timecard import TimecardEntry, Timecard, POSTTimecardEntry, ShorthandMapping
from datetime import datetime, timedelta


class UtilFunctions:
    def clean_timecard_data(self):
        tc = Timecard()
        tc.data = {}
        tc.save()


class TestTimecardEntry(UtilFunctions):
    def test_timecard_entry(self):
        tce = TimecardEntry(
            duration=timedelta(hours=1, minutes=30),
            day=datetime(2023, 11, 10),
        )
        output = tce.put
        rebuilt = TimecardEntry.build(output)
        rebuilt_output = rebuilt.put
        assert rebuilt_output['id'] == output['id']
        assert rebuilt_output['update_datetime'] == output['update_datetime']
        assert rebuilt_output['changelog'] == output['changelog']
        assert rebuilt_output['charge_code'] == output['charge_code']
        assert rebuilt_output['shorthand'] == output['shorthand']
        assert rebuilt_output['note'] == output['note']
        assert rebuilt_output['description'] == output['description']
        assert rebuilt_output['start_time'] == output['start_time']
        assert rebuilt_output['end_time'] == output['end_time']

class TestTimecard(UtilFunctions):
    def setUp(self):
        self.clean_timecard_data()

    def test_timecard_entry(self):
        self.clean_timecard_data()
        tc = Timecard()
        tc.save()
        tce = TimecardEntry(
            day=datetime(2023, 11, 10),
        )
        tc.add_entry(entry=tce)
        tc.save()
        tc.load()
        validate = tc.data

    def test_content(self):
        self.clean_timecard_data()
        x=1
        tc= Timecard()
        x=1
        initial_entry = TimecardEntry.build({
            'charge_code': 'MEETING.CHARGE.CODE.123',
            'shorthand': 'meeting',
            'note': 'standup',
            # description=,
            'start_time': '2020-01-01',
            # end_time=,
            'duration': '1.5',
            'day': '2023-11-10'
        })
        tc.add_entry(initial_entry)
        a = initial_entry.calculated_duration
        b = initial_entry.calculated_charge_code
        additional_entry = TimecardEntry.build({
            # 'charge_code': 'MEETING.CHARGE.CODE.123',
            'shorthand': 'working',
            # 'note': 'standup',
            # description=,
            'start_time': '2020-01-01',
            'end_time': '2020-01-01T01',
            # 'duration': '1.5 hr'
        })
        c = additional_entry.calculated_duration
        d = additional_entry.calculated_charge_code
        x=1
        x=1
        x=1
        x=1

    def test_only_start_and_end(self):
        x=1
        tc = Timecard()
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 10), start_time='2023-11-12T02:00:00Z', shorthand='general'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 10), end_time='2023-11-12T04:00:00Z', shorthand='general'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 10), start_time='2023-11-12T04:30:00Z', shorthand='general'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 10), end_time='2023-11-12T05:00:00Z', shorthand='general'))
        x=1
        charge_codes_per_day = tc.display_data()
        x=1

    def test_day_of_entries(self):
        x=1
        tc = Timecard()
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 12), start_time='2023-11-12T00:00:00Z', end_time='2023-11-12T01:00:00Z', shorthand='work'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 12), start_time='2023-11-12T02:00:00Z', duration=timedelta(hours=5, minutes=20), shorthand='general'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 12), end_time='2023-11-12T02:00:00Z', shorthand='work'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 12), duration=timedelta(hours=2, minutes=20), shorthand='meeting'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 11), duration=timedelta(hours=5, minutes=20), shorthand='work'))
        tc.add_entry(TimecardEntry(day=datetime(2023, 11, 11), duration=timedelta(hours=2), shorthand='meeting'))
        x=1
        charge_codes_per_day = tc.display_data()
        x=1

    def test_with_data(self):
        with open('/home/acobb/git/legba/data/timecard/dev_timesheet_for_use_and_testing.json', 'r') as jf:
            data = json.load(jf)

        # x=1
        # date_string = "2023-06-2"
        # data = {
        #     "2023-06-23": {
        #         "entries": [
        #             {
        #                 "start_time": "6",
        #                 "shorthand": "general"
        #             },
        #             {
        #                 "end_time": "1500",
        #                 "shorthand": "general"
        #             },

        #             {
        #                 "start_time": "0800",
        #                 "shorthand": "working"
        #             },
        #             {
        #                 "duration": 1,
        #                 "shorthand": "meeting"
        #             },
        #             {
        #                 "end_time": "09",
        #                 "shorthand": "work"
        #             },

        #             {
        #                 "end_time": "12:00",
        #                 "duration": 2,
        #                 "shorthand": "work"
        #             },
        #             {
        #                 "start_time": "15:00",
        #                 "duration": 2,
        #                 "shorthand": "meeting"
        #             }
        #         ]
        #     }
        # }

        timecard = Timecard()

        for day, entries in data.items():
            for entry in entries['entries']:
                entry['day'] = day
                post_obj = POSTTimecardEntry(**entry)
                te = post_obj.return_timecard_entry()
                timecard.add_entry(te)
        dd = timecard.display_data(day='2023-06')
        x=1

    def test_find_wrong_data(self):
        with open('/home/acobb/git/legba/data/timecard/dev_timesheet_for_use_and_testing.json', 'r') as jf:
            data = json.load(jf)

        timecard = Timecard()

        for day, entries in data.items():
            if day != '2023-06-16':
                continue
            x=1
            for entry in entries['entries']:
                entry['day'] = day
                post_obj = POSTTimecardEntry(**entry)
                te = post_obj.return_timecard_entry()
                timecard.add_entry(te)
        dd = timecard.display_data(day='2023-06-16')
        x=1

    def test_return(self):
        # results = [e.value for e in ShorthandMapping]
        # x=1
        # for i in results:
        #     a = ShorthandMapping(i)
        #     b = ShorthandMapping(i).name
        e = {k: getattr(ShorthandMapping, k).value for k in [ShorthandMapping(e).name for e in ShorthandMapping]}
        x=1
