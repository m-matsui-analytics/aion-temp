from typing import ClassVar

from rest_framework import serializers

from base.models import CompanyInfo


class CompanyInfoSerializer(serializers.ModelSerializer):
    """
    会社概要シリアライザ
    """

    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:  # noqa: D106
        model = CompanyInfo
        fields: ClassVar = [
            'company_name',
            'foundation_date',
            'capital',
            'post_code',
            'address_prefecture',
            'address_other',
            'ceo_name',
            'employee_size',
            'business_description',
            'industry',
            'revenue',
            'mission',
            'vision',
            'value',
        ]
        read_only_fields: ClassVar = ['company_name']
