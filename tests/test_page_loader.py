import os.path
import pytest
from page_loader import download
import requests_mock
from tests import FIXTURES_PATH


@pytest.mark.parametrize(
    "site,fixture_file",
    [("http://fixture.com", "some.html")],
)
def test_page_loader(site, fixture_file, tmp_path):
    with requests_mock.Mocker() as mocker:
        with open(os.path.join(FIXTURES_PATH, fixture_file)) as fixture:
            mocker.get(site, text=fixture.read())
            html_path = download(site, tmp_path)
            assert len(list(tmp_path.iterdir())) == 2
            assert os.path.isfile(html_path)
