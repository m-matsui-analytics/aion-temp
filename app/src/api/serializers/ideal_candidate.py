from typing import ClassVar

from rest_framework import serializers

from base.models import IdealCandidate


class IdealCandidateSerializer(serializers.ModelSerializer):
    """
    IdealCandidateのシリアライザ
    """

    class Meta:  # noqa: D106
        model = IdealCandidate

        fields: ClassVar = [
            'id',
            'company',
            'name',
            'age_min',
            'age_max',
            'work_value_1',
            'work_value_2',
            'work_value_3',
        ]

