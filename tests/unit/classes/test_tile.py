import pytest
from classes.tile import TargetElement, Tile, LinkElement


class TestTile:
    def test_details(self):
        t = Tile(
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
        x=1
        h1 = t.html
        h2 = t.html.return_string_version
        expected_str = '<div class="tile"><p>Name: Test<br>A test for testing<br><a href="https://test-url/extention/test-extension?qp1=qv-A&qp2=qv-B" target="_self">TestOrigin</a></p></div>'
        assert expected_str == t.html.return_string_version
        x=1
        assert True

    def test_empty(self):
        t = Tile()
        x=1
        h1 = t.html
        h2 = t.html.return_string_version
        x=1
        assert True