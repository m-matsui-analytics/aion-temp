
import os

import pytest

from tasks.jobs.content_analysis_updater import ContentAnalysisUpdater


@pytest.fixture
def set_up_ca_updater() -> None:
    """Fixture for setting up ContentAnalysisUpdater instance."""
    return ContentAnalysisUpdater(
        company_id=2,
        target_type=os.getenv("TARGET_TYPE_JOB_POSTING"),
        content_id=1,
        content_analysis_log_id=int,
        result={
            "summary": "test",
            "ideal_candidate_id_list": [
                {
                    "id": 1,
                    "reason": "test",
                    "relevance_level_id": 5
                },
                {
                    "id": 2,
                    "reason": "testtest",
                    "relevance_level_id": 4
                }
            ],
            "strength_id_list": [
                {
                    "id": 2,
                    "reason": "strength_id_list test",
                    "relevance_level_id": 3
                },
                {
                    "id": 3,
                    "reason": "strength_id_list testtest",
                    "relevance_level_id": 5
                }
            ]
        }
    )


# @pytest.mark.django_db(databases=["default"])
@pytest.mark.django_db
def test__validate_ideal_candidate_id_list(set_up_ca_updater: set_up_ca_updater) -> None:
    """Test __validate_ideal_candidate_id_list method."""
    set_up_ca_updater._ContentAnalysisUpdater__validate_ideal_candidate_id_list()

# @pytest.mark.django_db(databases=["default"])
@pytest.mark.django_db
def test__validate_strength_id_list(set_up_ca_updater: set_up_ca_updater) -> None:
    """Test __validate_strength_id_list method."""
    set_up_ca_updater._ContentAnalysisUpdater__validate_strength_id_list()

# @pytest.mark.django_db(databases=["default"])
@pytest.mark.django_db
def test_update_job_posting(set_up_ca_updater: set_up_ca_updater) -> None:
    """Test __update_job_posting method."""
    set_up_ca_updater._ContentAnalysisUpdater__update_job_posting()

# @pytest.mark.django_db(databases=["default"])
@pytest.mark.django_db
def test_update_recruitment_article(
        set_up_ca_updater: set_up_ca_updater,
    ) -> None:
    """Test __update_recruitment_article method."""
    set_up_ca_updater._ContentAnalysisUpdater__update_recruitment_article()

# @pytest.mark.django_db(databases=["default"])
@pytest.mark.django_db
def test_update(
        set_up_ca_updater: set_up_ca_updater,
    ) -> None:
    """Test update method."""
    set_up_ca_updater.update()

