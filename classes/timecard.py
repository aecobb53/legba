from pydantic import BaseModel


class Timecard:
    def __init__(self):
        x=1


class POSTTimecardEntry(BaseModel):
    example: str = None

