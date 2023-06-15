import pytest
from classes.timecard import TimecardEntry, Timecard, POSTTimecardEntry


class UtilFunctions:
    def clean_timecard_data(self):
        tc = Timecard()
        tc.data = {}
        tc.save()


class TestTimecardEntry(UtilFunctions):
    def test_timecard_entry(self):
        tce = TimecardEntry()
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
    def test_timecard_entry(self):
        self.clean_timecard_data()
        tc = Timecard()
        tc.save()
        tce = TimecardEntry()
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
            'duration': '1.5 hr'
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


