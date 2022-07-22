import tempfile
import pytest
from page_loader import download
from page_loader.refactors import create_name_for_downloads, parse_resource_format
import pook


@pytest.mark.parametrize(
    "site,reply",
    [
        (
            "https://ru.hexlet.io/courses",
            200
        )
    ],
)
@pook.on
def test_page_loader(site, reply):
    mock = pook.get("https://ru.hexlet.io/courses", reply=reply, response_json=1)
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
