import os.path
import pytest
from page_loader import download
import requests_mock
from tests import FIXTURES_PATH


@pytest.mark.parametrize(
    "site,fixture_html,fixture_img,fixture_scr,fixture_link",
    [
        (
            "http://fixture.com",
            "some.html",
            "some_img.png",
            "some_script.js",
            "some_link.css",
        )
    ],
)
def test_page_loader(
    site, fixture_html, fixture_img, fixture_scr, fixture_link, tmp_path
):
    with requests_mock.Mocker() as mocker:
        with open(os.path.join(FIXTURES_PATH, fixture_html)) as fixture:
            mocker.get(site, text=fixture.read())

        with open(os.path.join(FIXTURES_PATH, fixture_link), "rb") as fixture:
            mocker.get(
                "https://fixture.com/assets/application.css", content=fixture.read()
            )
            mocker.get("https://fixture.com/courses", content=fixture.read())

        with open(os.path.join(FIXTURES_PATH, fixture_scr), "rb") as fixture:
            mocker.get(
                "https://fixture.com/packs/js/runtime.js", content=fixture.read()
            )

        with open(os.path.join(FIXTURES_PATH, fixture_img), "rb") as fixture:
            mocker.get(
                "https://fixture.com/assets/professions/nodejs.png",
                content=fixture.read(),
            )

        html_path = download(site, tmp_path)
        dir_path = html_path[:-5] + "_files"

        assert len(list(tmp_path.iterdir())) == 2
        assert os.path.isfile(html_path)
        assert os.path.isdir(dir_path)
        assert len(list(os.listdir(dir_path))) == 4
