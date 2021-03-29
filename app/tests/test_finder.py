import pytest
from requests_mock import ANY, Mocker

from app.numbers.finder import get_number


@pytest.mark.parametrize('response, status, expected_number', [
    ('<div style="padding-bottom:5px;" class="">8 (495) 540-56-76</div>', 200, '84955405676'),
    ('<div style="padding-bottom:5px;" class="">8 3532 22-56-76</div>', 200, '83532225676'),
    ('<div style="padding-bottom:5px;" class="">(495) 660-83-17</div>', 200, '84956608317'),
    ('<div style="padding-bottom:5px;" class="">540-56-76</div>', 200, '84955405676'),
    ('Not found', 404, None),
])
def test_get_number(response, expected_number, status):
    with Mocker() as m:
        m.get(ANY, text=response, status_code=status)

        res = get_number("http://link.to")
        assert res == expected_number
