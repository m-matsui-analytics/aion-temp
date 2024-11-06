from typing import ClassVar

from rest_framework import serializers

from base.models import CompanyMedia


class CompanyMediaSerializer(serializers.Serializer):
    """
    CompanyMediaの登録用シリアライザ
    """

    media = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )

    def validate_media(self, value: list[int]) -> list[int]:
        """
        Validate each media value in the list
        """
        valid_choices = [choice[0] for choice in CompanyMedia.media.field.choices]
        invalid_values = [v for v in value if v not in valid_choices]

        if invalid_values:
            raise serializers.ValidationError(f"Invalid media values: {invalid_values}")

        return value

    def create(self, validated_data: dict) -> list[int]:
        """
        Create CompanyMedia entries for each media value
        """
        company = self.context['request'].user.company
        media_values = validated_data['media']
        created_media = []

        for media in media_values:
            if CompanyMedia.objects.filter(company=company, media=media).exists():
                raise serializers.ValidationError(f"Media {media} already exists")

            created_media_instance = CompanyMedia.objects.create(
                company=company, media=media
            )
            created_media.append(created_media_instance.media)

        return created_media

class CompanyMediaDeleteSerializer(serializers.Serializer):
    """
    CompanyMediaの削除用シリアライザ
    """

    media = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
    )

    def validate_media(self, value: list[int]) -> list[int]:
        """
        Validate that each media value exists in the company
        """
        company = self.context['request'].user.company
        existing_media = set(CompanyMedia.objects.filter(company=company)
                            .values_list('media', flat=True))

        # 存在しないmedia IDをチェック
        invalid_media = [media for media in value if media not in existing_media]
        if invalid_media:
            raise serializers.ValidationError(f"Media ID(s) {invalid_media} do not exist for this company.")

        return value
