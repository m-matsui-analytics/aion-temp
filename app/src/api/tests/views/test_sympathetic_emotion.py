from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_builder_user, create_normal_user

User = get_user_model()


class EmpathyEmotionViewTestCase(APITestCase):
    """
    Test case for `EmpathyEmotionView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        self.builder_user = create_builder_user()
        self.normal_user = create_normal_user()

        # 認証用クライアント
        self.client = APIClient()

    def test_get_empathy_emotion_by_builder_user(self) -> None:
        """
        `builder`グループのユーザーが「共感する感情」を取得できるかテスト
        """
        # `builder`グループユーザーで認証
        self.client.force_authenticate(user=self.builder_user)

        url = reverse("empathy_emotion")  # `urls.py`で定義された名前を使用
        response = self.client.get(url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_choices = [
            {"value": 1, "label": "転職に対する期待"},
            {"value": 2, "label": "現職に対する不満"},
            {"value": 3, "label": "転職に対する不安"},
        ]

        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_choices:
            raise ValueError("Response data does not match expected choices.")

    def test_get_empathy_emotion_by_normal_user(self) -> None:
        """
        `builder`グループに属していないユーザーが権限エラーとなるかテスト
        """
        # `builder`グループに属していないユーザーで認証
        self.client.force_authenticate(user=self.normal_user)

        url = reverse("empathy_emotion")
        response = self.client.get(url)

        # ステータスコードが403であることを確認
        if not response.status_code == status.HTTP_403_FORBIDDEN:
            raise ValueError("Status code is not 403.")

