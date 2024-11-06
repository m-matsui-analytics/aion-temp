import json
from pathlib import Path

from django.test import TestCase

from base.models.candidate import Candidate
from base.models.company import Company
from tasks.jobs.career_detail_updater import CareerDetailUpdater

TEST_DATA_DIR = Path("tasks/tests/data/")

class CareerDetailUpdaterTestCase(TestCase):
    """
    Test CareerDetailUpdater
    """

    def setUp(self):
        self.company = Company.objects.create(
            id = 2,
        )
        self.candidate = Candidate.objects.create(
            id = 2,
            company=self.company,
            company_candidate_id = 2,
        )

    def test_career_detail_updater(self):
        """Test CareerDetailUpdater"""
        print("test_career_detail_updater")
        with open(f"{TEST_DATA_DIR}/career_detail/2.json") as f:
            data = json.load(f)
        print(data)
        career_detail_updater = CareerDetailUpdater(
            candidate_id=data["candidate_id"],
            career_detail=data["career_detail"]
        )

        career_detail_updater.update()
        print("test_career_detail_updater end")
