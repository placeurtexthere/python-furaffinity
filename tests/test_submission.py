import pytest

import datetime
from bs4 import BeautifulSoup

from furaffinity.submission import FASubmission
from furaffinity.errors import *

with open("tests/resources/submission.html") as dummy:
    soup = BeautifulSoup(dummy, "html.parser")


def test_init():
    assert FASubmission(soup, '00001')


def test_basics():
    submission = FASubmission(soup, '00001')
    assert submission.title == "Test File"
    assert submission.uploader == "Fakeartist"
    assert submission.description == "This is a test file I made for foobar!"


def test_details():
    submission = FASubmission(soup, '00001')
    assert submission.category == "Artwork (Digital)"
    assert submission.theme == "General Furry Art"
    assert submission.species == "Unspecified / Any"
    assert submission.gender == "Other / Not Specified"


def test_stats():
    submission = FASubmission(soup, '00001')
    assert submission.favorites == 199
    assert submission.comments == 5
    assert submission.views == 1026
    assert submission.rating == "General"


def test_file():
    submission = FASubmission(soup, '00001')
    assert submission.file.url == "https://example.com/00001.jpg"
    assert submission.file.file_name == "00001.jpg"
    assert submission.file.file_extension == "jpg"


def test_thumb():
    submission = FASubmission(soup, '00001')
    assert submission.thumb.url == "https://example.com/00001-thumb.jpg"
    assert submission.thumb.file_name == "00001-thumb.jpg"
    assert submission.thumb.file_extension == "jpg"


def test_time():
    submission = FASubmission(soup, '00001')
    expected_time = datetime.datetime(2016, 10, 21, 3, 44, 00)

    assert submission.time_raw == "Oct 21st, 2016 03:44 AM"
    assert submission.time_parsed == expected_time
    assert submission.time_formatted == "21/10/2016 03:44"


def test_keywords():
    submission = FASubmission(soup, '00001')
    assert submission.keywords == ['Tag1', 'Tag2', 'Tag3']


def test_tagged():
    submission = FASubmission(soup, '00001')
    assert submission.tagged_users == ['foobar']


def test_errors():
    nf_soup = BeautifulSoup("<title>System Error</title>", "html.parser")
    nf_submission = FASubmission(nf_soup, "00001")

    with pytest.raises(SubmissionNotFoundError):
        nf_submission.check_errors()

    ip_soup = BeautifulSoup("<title>None</title> Your IP address has been banned.", "html.parser")
    ip_submission = FASubmission(ip_soup, "00001")

    with pytest.raises(IPBanError):
        ip_submission.check_errors()

    ma_soup = BeautifulSoup("<title>None</title> This submission contains Mature or Adult content", "html.parser")
    ma_submission = FASubmission(ma_soup, "00001")

    with pytest.raises(MaturityError):
        ma_submission.check_errors()

    ac_soup = BeautifulSoup("<title>None</title> You are not allowed to view this image", "html.parser")
    ac_submission = FASubmission(ac_soup, "00001")

    with pytest.raises(AccessError):
        ac_submission.check_errors()
