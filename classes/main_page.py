from wall import Wall
from mosaic import Mosaic, TrafficMosaic, IFSCMosaic
from tile import TargetElement, LinkElement, Tile
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

# ifsc_mosaic = IFSCMosaic()

# tile_1_content = HtmlList(
#     ordered=True,
#     internal=[
#         HtmlListItem(content='Janja Garnbret'),
#         HtmlListItem(content='Chaehyun Seo'),
#         HtmlListItem(content='Natalia Grossman'),
#         HtmlListItem(content='Laura Rogora'),
#         HtmlListItem(content='Brooke Raboutou'),
#     ]
# )
# tile_1_content = Paragraph(
#     internal=tile_1_content
# )
# ifsc_tile_1 = Tile(
#     name='WL5',
#     description='Current womans top 5 Lead rankings',
#     content=tile_1_content.return_string_version,
#     html_classes=['tile-ifsc']
# )
# ifsc_mosaic.add_tile(ifsc_tile_1)

# tile_2_content = HtmlList(
#     ordered=True,
#     internal=[
#         HtmlListItem(content='Janja Garnbret'),
#         HtmlListItem(content='Chaehyun Seo'),
#         HtmlListItem(content='Natalia Grossman'),
#         HtmlListItem(content='Laura Rogora'),
#         HtmlListItem(content='Brooke Raboutou'),
#     ]
# )
# tile_2_content = Paragraph(
#     internal=tile_2_content
# )
# ifsc_tile_2 = Tile(
#     name='WB5',
#     description='Current womans top 5 Bouldering rankings',
#     content=tile_2_content.return_string_version,
#     html_classes=['tile-ifsc']
# )
# ifsc_mosaic.add_tile(ifsc_tile_2)

# tile_3_content = HtmlList(
#     ordered=True,
#     internal=[
#         HtmlListItem(content='Janja Garnbret'),
#         HtmlListItem(content='Chaehyun Seo'),
#         HtmlListItem(content='Natalia Grossman'),
#         HtmlListItem(content='Laura Rogora'),
#         HtmlListItem(content='Brooke Raboutou'),
#     ]
# )
# tile_3_content = Paragraph(
#     internal=tile_3_content
# )
# ifsc_tile_3 = Tile(
#     name='WS5',
#     description='Current womans top 5 Spead rankings',
#     content=tile_3_content.return_string_version,
#     html_classes=['tile-ifsc']
# )
# ifsc_mosaic.add_tile(ifsc_tile_3)

# main_page.add_mosaic(ifsc_mosaic)

# a = ifsc_tile_1.put
# a2 = Tile.build(a)
# b = ifsc_tile_2.put
# b2 = Tile.build(b)
# c = ifsc_tile_3.put
# c2 = Tile.build(c)

# d = ifsc_mosaic.put
# d2 = IFSCMosaic.build(d)

# x=1

# with open('data/ifsc_mosaic.json', 'w') as jf:
#     jf.write(json.dumps(ifsc_mosaic.put, indent=4))

# with open('data/ifsc_mosaic.json', 'r') as jf:
#     ifsc_mosaic = IFSCMosaic.build(json.load(jf))
# main_page.add_mosaic(ifsc_mosaic)
for root, dirs, files in os.walk('data'):
    for fl in files:
        match = re.search(r'^([a-zA-Z0-9_]+)_mosaic\.json$', fl)
        if match:
            a = match.groups(0)
            x=1
            with open(os.path.join(root, fl), 'r') as jf:
                mosaic = Mosaic.build(json.load(jf))

            main_page.add_mosaic(mosaic)
        x=1

x=1

hr = HtmlReader()
data = hr.read_css_file('templates/main_page.css')
main_page.doc.styles.extend(data)

x=1

with open('testing.html', 'w') as hf:
    hf.write(main_page.html)

x=1


"""
Page colors (Base to content accent):
#272727
#747474
#FF652F
#FFE400
#14A76C
"""