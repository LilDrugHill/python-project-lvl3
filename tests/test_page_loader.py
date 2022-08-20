import os.path
import pytest
from page_loader import download
import requests_mock
from tests import FIXTURES_PATH


FIXTURES_AND_URLS_FOR_MOCKER = (
    ("some_img.png", "https://fixture.com/assets/professions/nodejs.png"),
    ("some_script.js", "https://fixture.com/packs/js/runtime.js"),
    ("some_link.css", "https://fixture.com/assets/application.css"),
    ("some_link.css", "https://fixture.com/courses"),
)


@pytest.mark.parametrize(
    "site,fixture_html",
    [("http://fixture.com", "some.html")],
)
def test_page_loader(site, fixture_html, tmp_path):
    with requests_mock.Mocker() as mocker:
        with open(os.path.join(FIXTURES_PATH, fixture_html)) as fixture:
            mocker.get(site, text=fixture.read())

        for fixture, url in FIXTURES_AND_URLS_FOR_MOCKER:
            with open(os.path.join(FIXTURES_PATH, fixture), "rb") as opened_fixture:
                mocker.get(url, content=opened_fixture.read())

        html_path = download(site, tmp_path)
        dir_path = html_path[:-5] + "_files"

        assert len(list(tmp_path.iterdir())) == 2
        assert os.path.isfile(html_path)
        assert os.path.isdir(dir_path)
        assert len(list(os.listdir(dir_path))) == 4
