from pathlib import Path

from django.contrib.auth import get_user_model
from django.utils.timezone import localtime
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import JobPosting, RecruitmentMedia


class JobPostingCreateTextView(APITestCase):
    """
    求人票作成（テキスト）APIのテスト
    """  # noqa: RUF002

    TARGET_URL = "/api/job_posting/text/"

    @classmethod
    def setUpClass(cls) -> None:
        """
        事前準備
        """
        # ユーザーを作成
        super().setUpClass()
        cls.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="test_user_password",
            company_id=1,
        )

    def test_create_success(self) -> None:
        """
        正常系
        """
        file_path = Path("api/tests/data/views/job_posting/create_text/1.txt")
        with Path.open(
            file_path,
            encoding="utf-8",
        ) as file:
            text = file.read()        # token= str(RefreshToken.for_user(self.user).access_token)
        self.client.force_authenticate(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        param = {
            "url": "https://example.com",
            "media": RecruitmentMedia.AMBI,
            "title": "テスト求人",
            "text": text,
        }
        response = self.client.post(
            self.TARGET_URL,
            param,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        JobPosting.objects.get(title="テスト求人")
