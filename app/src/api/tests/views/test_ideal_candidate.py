from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_normal_user
from base.models import IdealCandidate, WorkValue

User = get_user_model()


class IdealCandidateListViewTestCase(APITestCase):
    """
    Test case for `IdealCandidateListView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        # 一般ユーザーを作成
        self.normal_user = create_normal_user()

        # 仕事観を登録
        self.work_value_1 = WorkValue.objects.create(
            work_value="テスト用の働きがい1",
            description="テスト用の働きがい1の説明",
        )
        self.work_value_2 = WorkValue.objects.create(
            work_value="テスト用の働きがい2",
            description="テスト用の働きがい2の説明",
        )
        self.work_value_3 = WorkValue.objects.create(
            work_value="テスト用の働きがい3",
            description="テスト用の働きがい3の説明",
        )

        # 求める人物像を登録
        self.company = self.normal_user.company
        IdealCandidate.objects.create(
            company=self.company,
            name="テスト用の求める人物像",
            age_min=25,
            age_max=30,
            work_value_1=self.work_value_1,
        )

        # 認証用クライアント
        self.client = APIClient()
        self.client.force_authenticate(user=self.normal_user)

        self.url = reverse("ideal_candidate")

    def test_get_ideal_candidate(self) -> None:
        """
        ユーザーが所属する企業の求める人物像を取得できるかテスト
        """
        response = self.client.get(self.url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_data = [
            {
                "id": 1,
                "company": self.company.id,
                "name": "テスト用の求める人物像",
                "age_min": 25,
                "age_max": 30,
                "work_value_1": self.work_value_1.id,
                "work_value_2": None,
                "work_value_3": None,
            }
        ]
        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_data:
            raise ValueError("Response data does not match expected choices.")
