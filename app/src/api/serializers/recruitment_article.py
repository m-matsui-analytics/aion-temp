from typing import ClassVar

from rest_framework import serializers

from base.models import RecruitmentArticle


class RecruitmentArticleSerializer(serializers.ModelSerializer):
    """
    RecruitmentArticleの登録用シリアライザ
    """

    class Meta:  # noqa: D106
        model = RecruitmentArticle
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
    #     RecruitmentArticleの登録
    #     """
    #     print(validated_data)
    #     company = self.context['request'].user.company
    #     return RecruitmentArticle.objects.create(company=company, **validated_data)

class RecruitmentArticleListSerializer(serializers.ListSerializer):
    """
    RecruitmentArticleのリスト用シリアライザ
    """

    child = RecruitmentArticleSerializer()

    def validate(self, data: list) -> list:
        """
        リスト全体のバリデーション
        """
        for item in data:
            item_serializer = RecruitmentArticleSerializer(data=item)
            item_serializer.is_valid(raise_exception=True)
        return data

class RecruitmentArticleCreateURLSerializer(serializers.ModelSerializer):
    """
    RecruitmentArticleのURL登録用シリアライザ
    """

    url = serializers.URLField()

    class Meta:  # noqa: D106
        model = RecruitmentArticle
        fields: ClassVar = [
            "title",
            "url",
            "media",
        ]

    def create(self, validated_data: dict) -> list[int]:
        """
        RecruitmentArticleの登録
        """
        company = self.context['request'].user.company
        return RecruitmentArticle.objects.create(company=company, **validated_data)


class RecruitmentArticleCreateTextSerializer(serializers.ModelSerializer):
    """
    RecruitmentArticleのText登録用シリアライザ
    """

    class Meta:  # noqa: D106
        model = RecruitmentArticle
        fields: ClassVar = [
            "url",
            "title",
            "media",
        ]
    def create(self, validated_data: dict) -> list[int]:
        """
        RecruitmentArticleの登録
        """
        company = self.context['request'].user.company
        return RecruitmentArticle.objects.create(company=company, **validated_data)
