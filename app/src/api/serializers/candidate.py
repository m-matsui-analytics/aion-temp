from typing import ClassVar

from rest_framework import serializers

from base.models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    """
    会社概要シリアライザ
    """

    class Meta:  # noqa: D106
        model = Candidate
        fields: ClassVar = [
            'last_name',
            'first_name',
            'gender',
            'age',
            'prefecture',
            'industry',
            'occupation',
            'position',
            'current_company',
            'department',
            'job_title',
            'current_annual_income_min',
            'current_annual_income_max',
            'work_value_1',
            'work_value_2',
            'expectation_1',
            'expectation_2',
            'dissatisfaction_1',
            'dissatisfaction_2',
            'anxiety_1',
            'anxiety_2',
            'is_career_change',
            'preferred_annual_income',
        ]
