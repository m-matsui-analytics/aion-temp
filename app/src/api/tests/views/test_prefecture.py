from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_builder_user, create_normal_user

User = get_user_model()


class PrefectureViewTestCase(APITestCase):
    """
    Test case for `PrefectureView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        self.builder_user = create_builder_user()
        self.normal_user = create_normal_user()

        # 認証用クライアント
        self.client = APIClient()

    def test_get_prefecture_by_builder_user(self) -> None:
        """
        `builder`グループのユーザーが「都道府県」を取得できるかテスト
        """
        # `builder`グループユーザーで認証
        self.client.force_authenticate(user=self.builder_user)

        url = reverse("prefecture")  # `urls.py`で定義された名前を使用
        response = self.client.get(url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_choices = [
            {"value": 1, "label": "北海道"},
            {"value": 2, "label": "青森県"},
            {"value": 3, "label": "岩手県"},
            {"value": 4, "label": "宮城県"},
            {"value": 5, "label": "秋田県"},
            {"value": 6, "label": "山形県"},
            {"value": 7, "label": "福島県"},
            {"value": 8, "label": "茨城県"},
            {"value": 9, "label": "栃木県"},
            {"value": 10, "label": "群馬県"},
            {"value": 11, "label": "埼玉県"},
            {"value": 12, "label": "千葉県"},
            {"value": 13, "label": "東京都"},
            {"value": 14, "label": "神奈川県"},
            {"value": 15, "label": "新潟県"},
            {"value": 16, "label": "富山県"},
            {"value": 17, "label": "石川県"},
            {"value": 18, "label": "福井県"},
            {"value": 19, "label": "山梨県"},
            {"value": 20, "label": "長野県"},
            {"value": 21, "label": "岐阜県"},
            {"value": 22, "label": "静岡県"},
            {"value": 23, "label": "愛知県"},
            {"value": 24, "label": "三重県"},
            {"value": 25, "label": "滋賀県"},
            {"value": 26, "label": "京都府"},
            {"value": 27, "label": "大阪府"},
            {"value": 28, "label": "兵庫県"},
            {"value": 29, "label": "奈良県"},
            {"value": 30, "label": "和歌山県"},
            {"value": 31, "label": "鳥取県"},
            {"value": 32, "label": "島根県"},
            {"value": 33, "label": "岡山県"},
            {"value": 34, "label": "広島県"},
            {"value": 35, "label": "山口県"},
            {"value": 36, "label": "徳島県"},
            {"value": 37, "label": "香川県"},
            {"value": 38, "label": "愛媛県"},
            {"value": 39, "label": "高知県"},
            {"value": 40, "label": "福岡県"},
            {"value": 41, "label": "佐賀県"},
            {"value": 42, "label": "長崎県"},
            {"value": 43, "label": "熊本県"},
            {"value": 44, "label": "大分県"},
            {"value": 45, "label": "宮崎県"},
            {"value": 46, "label": "鹿児島県"},
            {"value": 47, "label": "沖縄県"},
            {"value": 99, "label": "海外"}
        ]

        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_choices:
            raise ValueError("Response data does not match expected choices.")

    def test_get_prefecture_by_normal_user(self) -> None:
        """
        `builder`グループに属していないユーザーが権限エラーとなるかテスト
        """
        # `builder`グループに属していないユーザーで認証
        self.client.force_authenticate(user=self.normal_user)

        url = reverse("prefecture")
        response = self.client.get(url)

        # ステータスコードが403であることを確認
        if not response.status_code == status.HTTP_403_FORBIDDEN:
            raise ValueError("Status code is not 403.")

