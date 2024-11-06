import pytest
from django.db import transaction

from base.models.company import Company
from base.models.ideal_candidate import IdealCandidate
from base.models.ideal_candidate_requirement import IdealCandidateRequirement


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_ideal_candidate(company: Company) -> None:
    with transaction.atomic():
        # IdealCandidateのレコードを作成
        ideal_candidate1 = IdealCandidate.objects.create(
            id=1,
            name='未経験',
            age_min=23,
            age_max=30,
            education=3,
            preferred_industry=1,
            preferred_occupation=8,
            current_position=6,
            current_annual_income=400,
            current_income_range_type=2,
            employment_status=3,
            company=company
        )

        ideal_candidate2 = IdealCandidate.objects.create(
            id=2,
            name='ジュニア層',
            age_min=20,
            age_max=32,
            education=3,
            preferred_industry=1,
            preferred_occupation=8,
            employment_status=3,
            company=company,
            desired_income_range_type=2,
            desired_annual_income=450
        )

        ideal_candidate3 = IdealCandidate.objects.create(
            id=3,
            name='ミドル層',
            age_min=28,
            age_max=35,
            education=3,
            employment_status=3,
            company=company,
            desired_income_range_type=2,
            desired_annual_income=600
        )

        # IdealCandidateRequirementのレコードを作成
        IdealCandidateRequirement.objects.bulk_create([
            IdealCandidateRequirement(
                id=1,
                requirement_category=99,
                recruitment='転職回数、20代は3回・30代は4回以内',
                requirement_level=1,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=2,
                requirement_category=99,
                recruitment='転職回数、20代は3回・30代は4回以内',
                requirement_level=1,
                ideal_candidate=ideal_candidate2
            ),
            IdealCandidateRequirement(
                id=3,
                requirement_category=2,
                recruitment='正社員としての就業経験（1年以上）',
                requirement_level=1,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=4,
                requirement_category=1,
                recruitment='基本的なITスキル（Excelでの四則演算、関数・ピボットテーブル、グラフ作成、PPTでのスライド作成など）',
                requirement_level=1,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=5,
                requirement_category=2,
                recruitment='データ分析やプログラミング(SQL/AWS/Python)に関する学習経験（大学時の授業やゼミ、オンライン授業、書籍学習など）',
                requirement_level=1,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=6,
                requirement_category=2,
                recruitment='プログラミング言語(Java/Python等)を用いた開発実務経験 1年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate2
            ),
            IdealCandidateRequirement(
                id=7,
                requirement_category=2,
                recruitment='SQL(MySQL/PostgreSQL等)を使用したデータ処理実務経験 1年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate2
            ),
            IdealCandidateRequirement(
                id=8,
                requirement_category=2,
                recruitment='BIツール(Tableau/Power BI等)を使用したデータ処理・集計・分析実務経験 1年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=9,
                requirement_category=2,
                recruitment='分析ツール(Python/R等)を使用した分析実務経験 1年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate2
            ),
            IdealCandidateRequirement(
                id=11,
                requirement_category=2,
                recruitment='SQL(MySQL/PostgreSQL等)を使用したデータ処理実務経験 3年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate3
            ),
            IdealCandidateRequirement(
                id=12,
                requirement_category=2,
                recruitment='プログラミング言語(Java/Python等)を用いた開発実務経験 3年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate3
            ),
            IdealCandidateRequirement(
                id=13,
                requirement_category=2,
                recruitment='BIツール(Tableau/Power BI等)を使用したデータ処理・集計・分析実務経験 3年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate3
            ),
            IdealCandidateRequirement(
                id=14,
                requirement_category=2,
                recruitment='分析ツール(Python/R等)を使用した分析実務経験 3年以上',
                requirement_level=3,
                ideal_candidate=ideal_candidate3
            ),
            IdealCandidateRequirement(
                id=15,
                requirement_category=99,
                recruitment='精神疾患NG',
                requirement_level=1,
                ideal_candidate=ideal_candidate1
            ),
            IdealCandidateRequirement(
                id=16,
                requirement_category=99,
                recruitment='精神疾患NG',
                requirement_level=1,
                ideal_candidate=ideal_candidate3
            ),
            IdealCandidateRequirement(
                id=17,
                requirement_category=99,
                recruitment='精神疾患NG',
                requirement_level=1,
                ideal_candidate=ideal_candidate2
            )
        ])
