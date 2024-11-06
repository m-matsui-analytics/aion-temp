from typing import ClassVar

from rest_framework import serializers

from base.models import JobPosting


class JobPostingSerializer(serializers.ModelSerializer):
    """
    JobPostingの登録用シリアライザ
    """

    class Meta:  # noqa: D106
        model = JobPosting
        fields: ClassVar = [
            "title",
            "url",
            "media",
            "analysis_status",
        ]
        read_only_fields: ClassVar = [
            "analysis_status",
        ]
    # def create(self, validated_data: dict) -> list[int]:
    #     """
    #     JobPostingの登録
    #     """
    #     print(validated_data)
    #     company = self.context['request'].user.company
    #     return JobPosting.objects.create(company=company, **validated_data)

class JobPostingListSerializer(serializers.ListSerializer):
    """
    JobPostingのリスト用シリアライザ
    """

    child = JobPostingSerializer()

    def validate(self, data: list) -> list:
        """
        リスト全体のバリデーション
        """
        for item in data:
            item_serializer = JobPostingSerializer(data=item)
            item_serializer.is_valid(raise_exception=True)
        return data

class JobPostingCreateURLSerializer(serializers.ModelSerializer):
    """
    JobPostingのURL登録用シリアライザ
    """

    url = serializers.URLField()

    class Meta:  # noqa: D106
        model = JobPosting
        fields: ClassVar = [
            "title",
            "url",
            "media",
        ]

    def create(self, validated_data: dict) -> list[int]:
        """
        JobPostingの登録
        """
        company = self.context['request'].user.company
        return JobPosting.objects.create(company=company, **validated_data)


class JobPostingCreateTextSerializer(serializers.ModelSerializer):
    """
    JobPostingのText登録用シリアライザ
    """

    class Meta:  # noqa: D106
        model = JobPosting
        fields: ClassVar = [
            "url",
            "title",
            "media",
        ]
    def create(self, validated_data: dict) -> list[int]:
        """
        JobPostingの登録
        """
        company = self.context['request'].user.company
        return JobPosting.objects.create(company=company, **validated_data)
