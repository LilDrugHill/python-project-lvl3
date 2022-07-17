import tempfile
import pytest
from page_loader import download
from page_loader.page_loader import parse_name
import pook


@pytest.mark.parametrize("site", ["https://ru.hexlet.io/courses"])
@pook.on
def test_page_loader(site):
    mock = pook.get(
        "https://ru.hexlet.io/courses",
        reply=200,
        response_json={"it's": "done!"}
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        with open(download(site, tmp_dir)) as down_site_path:
            downloaded = down_site_path.read()
        assert downloaded == '{\n    "it\'s": "done!"\n}'
        assert mock.calls == 1


@pytest.mark.parametrize(
    "site,downloaded_file_name",
    [
        (
            "https://ru.hexlet.io/projects/51/members/23405",
            "ru-hexlet-io-projects-51-members-23405.html",
        ),
        ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses.html"),
    ],
)
def test_parse_name(site, downloaded_file_name):
    assert parse_name(site) == downloaded_file_name
