import json
from pathlib import Path
import typing

from django.test import TestCase
import pytest

from base.models.candidate import Candidate
from base.models.choices import RecruitmentMedia
from base.models.company import Company
from base.models.ideal_candidate import IdealCandidate
from base.models.scout import Scout
from tasks.jobs.ideal_candidate_match_updater import IdealCandidateMatchUpdater
from tasks.tests.data.export import IdealCandidateMatchData

from unittest.mock import patch

@pytest.fixture
def icm_updater():
    """Fixture for setting up IdealCandidateMatchUpdater instance."""
    return IdealCandidateMatchUpdater(
        mail_gen_log_id=2,
        candidate_id=2
    )

def test_init(icm_updater):
    """Test __init__ method."""
    assert icm_updater.mail_gen_log_id == 2
    assert icm_updater.candidate_id == 2
    assert icm_updater.ideal_candidate_id is None
    assert icm_updater.ideal_candidate is None
    assert icm_updater.matching_rate is None
    assert icm_updater.is_matched is None
    assert icm_updater.reason is None

@pytest.mark.django_db
def test_update(icm_updater):
    """Test update method."""
    # Create a sample IdealCandidate in the database
    ideal_candidate = IdealCandidate.objects.create(id=2, company_id=1)
    icm_updater.ideal_candidate = ideal_candidate
    icm_updater.matching_rate = 0.5
    icm_updater.is_matched = True
    icm_updater.reason = "reason"

    with patch.object(Scout.objects, "filter") as mock_filter:
        icm_updater.update()
        mock_filter.assert_called_once_with(candidate_id=2)
        mock_filter.return_value.update.assert_called_once_with(
            ideal_candidate=ideal_candidate,
            matching_rate=0.5,
            is_matched=True,
            reason="reason"
        )

@pytest.mark.django_db
def test_no_ideal_candidate_id(icm_updater):
    """Test when ideal_candidate_id is missing in the message body."""
    message_body = {
        "candidate_id": 2
    }

    with patch.object(icm_updater, "log_error") as mock_log_error:
        icm_updater.validate_ideal_candidate_id(message_body)
        mock_log_error.assert_called_once_with("no ideal_candidate_id")
        assert icm_updater.ideal_candidate_id is None

@pytest.mark.django_db
def test_ideal_candidate_id_not_int(icm_updater):
    """Test when ideal_candidate_id is not an integer."""
    message_body = {
        "ideal_candidate_id": "not_an_int",  # Not an integer
        "candidate_id": 2
    }

    with patch.object(icm_updater, "log_error") as mock_log_error:
        icm_updater.validate_ideal_candidate_id(message_body)
        mock_log_error.assert_called_once_with("ideal_candidate_id is not int")
        assert icm_updater.ideal_candidate_id is None

@pytest.mark.django_db
def test_ideal_candidate_id_not_found(icm_updater):
    """Test when ideal_candidate_id does not exist in the database."""
    message_body = {
        "ideal_candidate_id": 999,  # Non-existent ID
        "candidate_id": 2
    }

    with patch.object(icm_updater, "log_error") as mock_log_error:
        icm_updater.validate_ideal_candidate_id(message_body)
        mock_log_error.assert_called_once_with("ideal_candidate_id is not found")
        assert icm_updater.ideal_candidate is None

@pytest.mark.django_db
def test_ideal_candidate_id_found(icm_updater):
    """Test when ideal_candidate_id exists in the database."""
    # Create a sample IdealCandidate in the database
    ideal_candidate = IdealCandidate.objects.create(id=2, company_id=1)
    message_body = {
        "ideal_candidate_id": ideal_candidate.id,
        "candidate_id": 2
    }

    with patch.object(icm_updater, "log_error") as mock_log_error:
        icm_updater.validate_ideal_candidate_id(message_body)
        mock_log_error.assert_not_called()  # No error should be logged
        assert icm_updater.ideal_candidate_id is None
