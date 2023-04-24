from classes.wall import Wall
from classes.mosaic import Mosaic, TrafficMosaic, IFSCMosaic
from classes.tile import TargetElement, LinkElement, Tile
from phtml import *
import json
import os
import re


color_scheme = {
    'background': '#272727',
    'background-hilight': '#747474',
    'content-colors': [
        '#FF652F',
        '#FFE400',
        '#14A76C',
    ],
}

color_scheme = {
    'background-color': '#272727',
    # 'background-hilight': '#747474',
    # 'content-colors': [
    #     '#FF652F',
    #     '#FFE400',
    #     '#14A76C',
    # ],
}

main_page = Wall(
    color_scheme=color_scheme
)

for root, dirs, files in os.walk('data'):
    for fl in files:
        match = re.search(r'^([a-zA-Z0-9_]+)_mosaic\.json$', fl)
        if match:
            with open(os.path.join(root, fl), 'r') as jf:
                mosaic = Mosaic.build(json.load(jf))
            main_page.add_mosaic(mosaic)

hr = HtmlReader()
data = hr.read_css_file('templates/main_page.css')
main_page.doc.styles.extend(data)

with open('templates/main_page.html', 'w') as hf:
    hf.write(main_page.html)

"""
Page colors (Base to content accent):
#272727
#747474
#FF652F
#FFE400
#14A76C
"""