from pydantic import BaseModel
from typing import List
from enum import Enum
import json
import re
import os
from datetime import datetime

class Event(BaseModel):
    name: str
    venue: str
    city: str
    address: str
    event_type: str


