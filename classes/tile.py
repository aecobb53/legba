from lib2to3.pytree import Base
from pydantic import BaseModel
from typing import List, Dict
from enum import Enum
import json
import re
import os
from datetime import datetime
import phtml


class TargetElement(Enum):
    BLANK = '_blank' # New window or tab
    PARENT = '_parent' # Same frame as was clicked in
    SELF = '_self' # Parent frame # This is default
    TOP = '_top' # Full body of the window
    DEFAULT = None

class LinkElement(BaseModel):
    id: str = None
    link: str
    extension: str = None
    parameters: Dict = {}
    target: TargetElement = TargetElement.DEFAULT
    name: str = None
    description: str = None

    @property
    def put(self):
        output = {
            'id': self.id,
            'link': self.link,
            'extension': self.extension,
            'parameters': self.parameters,
            'target': self.target.key,
            'name': self.name,
            'description': self.description,
        }
        return output

    @property
    def url(self):
        url = self.link
        if self.extension:
            if url.endswith('/') or self.extension.startswith('/'):
                url += self.extension
            else:
                url += '/' + self.extension
        if self.parameters:
            params = []
            for key, value in self.parameters.items():
                params.append(f"{key}={value}")
            url += f"?{'&'.join(params)}"
        return url

    @property
    def html(self):
        output = phtml.Link(
            href=self.url,
        )
        if self.name is not None:
            output.internal.append(self.name)
        elif self.description is not None:
            output.internal.append(self.description)
        else:
            output.internal.append('Link')
        if self.target != TargetElement.DEFAULT:
            output.attributes['target'] = self.target.value
        return output

    @classmethod
    def build(cls, dct):
        obj = cls()
        return obj


class Tile(BaseModel):
    id: str = None
    name: str = None
    description: str = None
    links: List[LinkElement] = []
    files: List[Dict] = []
    tags: List[Dict] = []
    content: str = None

    version: int = 0
    notes: List[str] = []
    changelog: List[str] = []

    html_classes: List[str] = []
    html_styles: Dict = {}

    mutated = False

    @property
    def put(self):
        output = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "links": self.links,
            "files": self.files,
            "tags": self.tags,
            "content": self.content,
            "version": self.version,
            "notes": self.notes,
            "changelog": self.changelog,
            "html_classes": self.html_classes,
            "html_styles": self.html_styles,
            "mutated": self.mutated,
        }
        return output

    @property
    def html(self):
        output = phtml.Div()
        output.add_class('tile')

        # background_style = phtml.Style(
        #     style_details={
        #         'border-radius': '25px',
        #         'background': 'green',
        #         'padding': '10px',
        #         'margin': '20 px',
        #         'max-width': '25%',
        #         'max-height': '1000px',
        #     }
        # )
        # output.add_style(style_obj=background_style)
        if self.html_classes:
            for h_class in self.html_classes:
                output.add_class(h_class)
        if self.html_styles:
            for name, style in self.html_styles.items():
                output.add_style(phtml.Style(name=name, style_details=style))

        content = phtml.Paragraph()
        details = [
            f"Name: {self.name if self.name is not None else 'N/A'}",
            f"{self.description if self.description is not None else 'No description'}",
        ]
        if self.content:
            details.append(self.content)
        for link in self.links:
            details.append(link.html)
            # for descriptor, link in link_kv.items():
            #     anchor = phtml.Link(
            #         href=link,
            #         internal=descriptor
            #     )
            #     details.append(anchor)
        x=1
        for index, deet in enumerate(details):
            content.internal.append(deet)
            if index < len(details) - 1:
                content.internal.append(phtml.LineBreak())
        output.internal.append(content)

        return output

    @classmethod
    def build(cls, dct):
        obj = cls(
            id=dct.get('id'),
            name=dct.get('name'),
            description=dct.get('description'),
            links=dct.get('links'),
            files=dct.get('files'),
            tags=dct.get('tags'),
            content=dct.get('content'),
            version=dct.get('version'),
            notes=dct.get('notes'),
            changelog=dct.get('changelog'),
            html_classes=dct.get('html_classes'),
            html_styles=dct.get('html_styles'),
            mutated=dct.get('mutated'),
        )
        return obj
