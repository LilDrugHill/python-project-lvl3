import tempfile
import pytest
from page_loader import download
from page_loader.refactors import create_name_for_downloads, parse_resource_format
import pook
import re


@pytest.mark.parametrize("site,reply,response", [("https://ru.hexlet.io/courses", 200, '/Users/lildrugdgugstyle/python-project-lvl3/tests/fixtures/some.html')])
@pook.on
def test_page_loader(site, reply, response):
    with open(response) as fixture_html:
        data = fixture_html.read()
        mock = pook.get(
            "https://ru.hexlet.io/courses", reply=reply, response_json=data
        )
    with tempfile.TemporaryDirectory() as tmp_dir:
        html_file_path, _ = download(site, tmp_dir)
        assert mock.calls == 1


@pytest.mark.parametrize(
    "site,downloaded_file_name,parser",
    [
        (
            "https://ru.hexlet.io/projects/51/members/23405",
            "ru-hexlet-io-projects-51-members-23405",
            create_name_for_downloads,
        ),
        (
            "https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjhlY2MwOTdjZGY2YzVjMDI2OTYwMDI2ZGRiYjQ4MjMwLmpwZyIsInN0b3JhZ2UiOiJjYWNoZSJ9",
            "cdn2-hexlet-io-derivations-image-original-eyJpZCI6IjhlY2MwOTdjZGY2YzVjMDI2OTYwMDI2ZGRiYjQ4MjMwLmpwZyIsInN0b3JhZ2UiOiJjYWNoZSJ9",
            parse_resource_format,
        ),
    ],
)
def test_parse_name(site, downloaded_file_name, parser):
    assert parser(site) == downloaded_file_name
