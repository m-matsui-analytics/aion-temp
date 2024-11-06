from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_builder_user, create_normal_user

User = get_user_model()


class OccupationViewTestCase(APITestCase):
    """
    Test case for `OccupationView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        self.builder_user = create_builder_user()
        self.normal_user = create_normal_user()

        # 認証用クライアント
        self.client = APIClient()

    def test_get_occupation_by_builder_user(self) -> None:
        """
        `builder`グループのユーザーが「職業」を取得できるかテスト
        """
        # `builder`グループユーザーで認証
        self.client.force_authenticate(user=self.builder_user)

        url = reverse("occupation")  # `urls.py`で定義された名前を使用
        response = self.client.get(url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_choices = [
            {"value": 1, "label": "経営"},
            {"value": 2, "label": "管理"},
            {"value": 3, "label": "マーケティング"},
            {"value": 4, "label": "営業"},
            {"value": 5, "label": "コンサルタント"},
            {"value": 6, "label": "ITコンサルタント"},
            {"value": 7, "label": "専門職"},
            {"value": 8, "label": "IT技術職"},
            {"value": 9, "label": "ゲーム"},
            {"value": 10, "label": "電気・電子"},
            {"value": 11, "label": "半導体"},
            {"value": 12, "label": "機械"},
            {"value": 13, "label": "化学"},
            {"value": 14, "label": "金融"},
            {"value": 15, "label": "研究・臨床開発・治験"},
            {"value": 16, "label": "建築・土木"},
            {"value": 17, "label": "人事"},
            {"value": 18, "label": "サービス"},
            {"value": 19, "label": "プロジェクト管理"},
            {"value": 20, "label": "Webサービス・制作"},
            {"value": 21, "label": "デジタルマーケティング"},
            {"value": 22, "label": "広告"},
            {"value": 23, "label": "新聞・出版"},
            {"value": 24, "label": "テレビ・放送・映像・音響"},
            {"value": 25, "label": "デザイン"},
            {"value": 26, "label": "素材"},
            {"value": 27, "label": "食品"},
            {"value": 28, "label": "化粧品"},
            {"value": 29, "label": "日用品"},
            {"value": 30, "label": "不動産"},
            {"value": 31, "label": "施工管理"},
            {"value": 32, "label": "医療営業"},
            {"value": 33, "label": "生産管理・品質管理・品質保証"},
            {"value": 34, "label": "学術・PMS・薬事"},
            {"value": 35, "label": "医療・看護・薬剤"},
            {"value": 99, "label": "不明"}
        ]

        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_choices:
            raise ValueError("Response data does not match expected choices.")

    def test_get_occupation_by_normal_user(self) -> None:
        """
        `builder`グループに属していないユーザーが権限エラーとなるかテスト
        """
        # `builder`グループに属していないユーザーで認証
        self.client.force_authenticate(user=self.normal_user)

        url = reverse("occupation")
        response = self.client.get(url)

        # ステータスコードが403であることを確認
        if not response.status_code == status.HTTP_403_FORBIDDEN:
            raise ValueError("Status code is not 403.")

