from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_builder_user, create_normal_user

User = get_user_model()


class IndustryViewTestCase(APITestCase):
    """
    Test case for `IndustryView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        self.builder_user = create_builder_user()
        self.normal_user = create_normal_user()

        # 認証用クライアント
        self.client = APIClient()

    def test_get_industry_by_builder_user(self) -> None:
        """
        `builder`グループのユーザーが「業種」を取得できるかテスト
        """
        # `builder`グループユーザーで認証
        self.client.force_authenticate(user=self.builder_user)

        url = reverse("industry")  # `urls.py`で定義された名前を使用
        response = self.client.get(url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_choices = [
            {"value": 1, "label": "IT・インターネット"},
            {"value": 2, "label": "メーカー"},
            {"value": 3, "label": "商社"},
            {"value": 4, "label": "流通・小売"},
            {"value": 5, "label": "コンサルティング"},
            {"value": 6, "label": "マスコミ・メディア"},
            {"value": 7, "label": "エンターテインメント"},
            {"value": 8, "label": "金融"},
            {"value": 9, "label": "建設"},
            {"value": 10, "label": "メディカル"},
            {"value": 11, "label": "エネルギー"},
            {"value": 12, "label": "保険"},
            {"value": 13, "label": "不動産"},
            {"value": 14, "label": "士業"},
            {"value": 15, "label": "サービス"},
            {"value": 16, "label": "運輸・交通"},
            {"value": 17, "label": "物流・倉庫"},
            {"value": 99, "label": "その他（教育・官公庁）など"}  # noqa: RUF001
        ]

        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_choices:
            raise ValueError("Response data does not match expected choices.")

    def test_get_industry_by_normal_user(self) -> None:
        """
        `builder`グループに属していないユーザーが権限エラーとなるかテスト
        """
        # `builder`グループに属していないユーザーで認証
        self.client.force_authenticate(user=self.normal_user)

        url = reverse("industry")
        response = self.client.get(url)

        # ステータスコードが403であることを確認
        if not response.status_code == status.HTTP_403_FORBIDDEN:
            raise ValueError("Status code is not 403.")

