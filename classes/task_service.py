import enum
import os
import re
import json

from pydantic import BaseModel, ValidationError
from enum import Enum
from typing import List, Union, Dict
from datetime import datetime, timedelta


class TaskServicePayload(BaseModel):
    source: str
    datetime: str
    json_content: Dict

    @classmethod
    def build(cls, dct):
        content = {
            'source': dct['source'],
            'datetime': dct['datetime'],
            'json_content': dct['json_content'],
        }
        obj = cls(**content)
        return obj

    def put(self):
        content = {
            'source': self.source,
            'datetime': self.datetime,
            'json_content': self.json_content,
        }
        return content

def save_task_service_payload(obj, logit):
    task_service_data = 'data/task_service.json'
    logit.info(f'About to write the {task_service_data} file')
    with open(task_service_data, 'w') as tf:
        tf.write(json.dumps(obj.put()))

def load_task_service_payload(logit):
    task_service_data = 'data/task_service.json'
    logit.info(f'About to load the {task_service_data} file')
    with open(task_service_data, 'r') as tf:
        obj = TaskServicePayload.build(json.load(tf))
    return obj
