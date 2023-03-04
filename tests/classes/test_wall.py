import pytest
from classes.wall import Wall
from classes.mosaic import Mosaic, TrafficMosaic
from classes.tile import TargetElement, LinkElement, Tile

def test_simple_wall():
    w = Wall()
    expected_html = '<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>\n</body>\n</html>'
    assert expected_html == w.html
    x=1

def test_mosaic():
    w = Wall()
    mosaic = Mosaic()
    w.add_mosaic(mosaic)
    with open('deleteme.html', 'w') as hf:
        hf.write(w.html)
    x=1

def test_traffic_mosaic():
    w = Wall()
    mosaic = TrafficMosaic()
    w.add_mosaic(mosaic)
    with open('deleteme.html', 'w') as hf:
        hf.write(w.html)
    x=1

def test_traffic_mosaic_with_data():
    w = Wall()
    mosaic = TrafficMosaic()
    tile = Tile(
        name='Test',
        description='A test for testing',
        links=[
            LinkElement(
                name='TestOrigin',
                description='Origin link for testing',
                link='https://test-url/extention',
                extension='test-extension',
                parameters={
                    'qp1': 'qv-A',
                    'qp2': 'qv-B',
                },
                target=TargetElement.SELF
            )
        ]
    )
    mosaic.add_tile(tile=tile)
    w.add_mosaic(mosaic)
    with open('deleteme.html', 'w') as hf:
        hf.write(w.html)
    x=1


