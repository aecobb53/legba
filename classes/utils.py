import re

from datetime import datetime, timedelta
from pytz import timezone

from phtml import HtmlReader


config = {
    'time_zones': {
        "Z": "UTC",
        "M": "America/Denver",
    }
}

# def read_css_file(path):
#     with open(path, 'r') as cf:

def parse_time_str(time_s):
    re_datetime = r'^(\d{4})-?(\d{2})?-?(\d{2})?T?(\d{2})?[:]?(\d{2})?[:]?(\d{2})?\.?(\d+)?([A-z]+|[\+-]\d{2}(:\d{2})?)?'
    search = re.match(re_datetime, time_s)
    time = []
    if search is None:
        raise ValueError('Time is not parsable')
    for i in range(1,4):
        try:
            group = search.group(i)
            if group is None:
                raise TypeError
            time.append(group)
        except TypeError:
            time.append('01')
        except IndexError:
            time.append('01')
    for i in range(4,7):
        try:
            group = search.group(i)
            if group is None:
                raise TypeError
            time.append(group)
        except TypeError:
            time.append('00')
        except IndexError:
            time.append('00')
    try:
        group = search.group(7)[:6]
        time.append(group)
    except TypeError:
        time.append('0')
    except IndexError:
        time.append('0')

    if search.group(8):
        group1 = search.group(8)
        hours = None
        if group1:
            if group1.startswith('+'):
                group1 = group1[1:]
            if ':' in group1:
                group1 = group1.split(':')[0]
            try:
                hours = int(group1)
                if hours < 0:
                    hours = f"-{str(abs(hours)).zfill(2)}"
                elif hours > 0:
                    hours = f"+{str(abs(hours)).zfill(2)}"
                else:
                    hours = '+00'
            except ValueError:
                pass
        group2 = search.group(9)
        minutes = '00'
        if group2:
            if group2.startswith(':'):
                minutes = str(int(group2[1:])).zfill(2)
        if hours is None:
            if group1 in config['time_zones']:
                group1 = config['time_zones'][group1]
            tz = timezone(group1)
            hours = int(tz.utcoffset(datetime.now()).total_seconds() / (60*60))
            if hours < 0:
                hours = f"-{str(abs(hours)).zfill(2)}"
            elif hours > 0:
                hours = f"+{str(abs(hours)).zfill(2)}"
            else:
                hours = '+00'
        offset = f"{hours}{minutes}"
    else:
        offset = '+0000'
    time.append(offset)
    # print(time)

    time = '-'.join(time)
    obj = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S-%f-%z')
    return obj

def parse_datetime_shorthand(time_s):
    time_items = {
        'years': ['year', 'yr', 'y'],
        'months': ['month', 'mon'],
        'days': ['day', 'd'],
        'hours': ['hour', 'hr', 'h'],
        'minutes': ['minute', 'min', 'm'],
        'seconds': ['second', 'sec', 's'],
    }
    time = None
    for time_type, possible_strings in time_items.items():
        searcher1 = f"\d+\.?\d*"
        searcher2 = f"{'|'.join([i for i in possible_strings])}"
        match = re.search(rf'({searcher1})\s+({searcher2})', time_s)
        if match:
            if '.' in match.groups(0)[0]:
                value = float(match.groups(0)[0])
            else:
                value = int(match.groups(0)[0])
            value = {time_type: value}
            time = timedelta(**value)
    return time

def parse_potential_timestring(time_s):
    if time_s is None:
        return None
    time = None
    try:
        time = parse_datetime_string(time_s)
    except ValueError:
        pass
    if time is None:
        try:
            time = parse_datetime_shorthand(time_s)
        except Exception as err:
            x=1
    return time

