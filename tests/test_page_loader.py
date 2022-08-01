import os.path
import pytest
from page_loader import download
from page_loader.names_and_url_parsers import create_name_for_downloads, parse_resource_format
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


@pytest.mark.parametrize(
    "site,downloaded_file_name,parser",
    [
        (
            "https://ru.hexlet.io/projects/51/members/23405",
            "ru-hexlet-io-projects-51-members-23405",
            create_name_for_downloads,
        ),
        (
            "https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjhlY2MwOTdjZGY2\
YzVjMDI2OTYwMDI2ZGRiYjQ4MjMwLmpwZyIsInN0b3JhZ2UiOiJjYWNoZSJ9",
            "cdn2-hexlet-io-derivations-image-original-eyJpZCI6IjhlY2Mw\
OTdjZGY2YzVjMDI2OTYwMDI2ZGRiYjQ4MjMwLmpwZyIsInN0b3JhZ2UiOiJjYWNoZSJ9",
            parse_resource_format,
        ),
    ],
)
def test_parse_name(site, downloaded_file_name, parser):
    assert parser(site) == downloaded_file_name
