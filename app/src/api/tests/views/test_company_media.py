from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.tests.helpers import create_normal_user
from base.models import CompanyMedia, RecruitmentMedia

User = get_user_model()


class CompanyMediaViewTestCase(APITestCase):
    """
    Test case for `CompanyMediaView`.
    """

    def setUp(self) -> None:
        """
        テスト用のデータのセットアップ
        """
        self.normal_user = create_normal_user()

        # 利用媒体を登録
        company = self.normal_user.company
        CompanyMedia.objects.create(
            company=company,
            media=RecruitmentMedia.AMBI,
        )
        CompanyMedia.objects.create(
            company=company,
            media=RecruitmentMedia.RICRUIT,
        )

        # 認証用クライアント
        self.client = APIClient()
        self.client.force_authenticate(user=self.normal_user)

        self.url = reverse("company_media")

    def test_get_company_meidia(self) -> None:
        """
        ユーザーが所属する企業の利用媒体を取得できるかテスト
        """
        response = self.client.get(self.url)

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        # 期待される値を直接定義
        expected_data = [
            RecruitmentMedia.AMBI,
            RecruitmentMedia.RICRUIT
        ]

        # レスポンスデータと期待値が一致するか確認
        if not response.data == expected_data:
            raise ValueError("Response data does not match expected choices.")

    def test_post_company_media(self) -> None:
        """
        ユーザーが所属する企業の利用媒体を登録できるかテスト
        """
        media_list = [
            RecruitmentMedia.BIZREACH.value,
            RecruitmentMedia.OPEN_WORK.value,
        ]
        data = {
            "media": media_list
        }

        response = self.client.post(self.url, data=data, format='json')

        # ステータスコードが201であることを確認
        if not response.status_code == status.HTTP_201_CREATED:
            raise ValueError("Status code is not 201.")

        media_list += [
            RecruitmentMedia.AMBI.value,
            RecruitmentMedia.RICRUIT.value,
        ]

        response_media_list = response.data.get('media')

        # レスポンスデータと期待値が一致するか確認
        if not response_media_list.sort() == media_list.sort():
            raise ValueError("Response data does not match the posted data.")

    def test_post_company_media_invalid_data(self) -> None:
        """
        (異常系) 登録: 媒体IDが存在しない場合
        """
        media_list = [
            RecruitmentMedia.BIZREACH.value,
            20
        ]
        data = {
            "media": media_list
        }

        response = self.client.post(self.url, data=data, format='json')

        # ステータスコードが400であることを確認
        if not response.status_code == status.HTTP_400_BAD_REQUEST:
            raise ValueError("Status code is not 400.")

    def test_post_company_media_duplicate_data(self) -> None:
        """
        (異常系) 登録: 重複した媒体IDが存在する場合
        """
        media_list = [
            RecruitmentMedia.AMBI.value,
        ]
        data = {
            "media": media_list
        }

        response = self.client.post(self.url, data=data, format='json')
        # ステータスコードが400であることを確認
        if not response.status_code == status.HTTP_400_BAD_REQUEST:
            raise ValueError("Status code is not 400.")

    def test_delete_company_media(self) -> None:
        """
        ユーザーが所属する企業の利用媒体を削除できるかテスト
        """
        media_list = [
            RecruitmentMedia.AMBI.value,
            RecruitmentMedia.RICRUIT.value,
        ]
        data = {
            "media": media_list
        }
        response = self.client.delete(self.url, data=data, format='json')

        # ステータスコードが200であることを確認
        if not response.status_code == status.HTTP_200_OK:
            raise ValueError("Status code is not 200.")

        expected_data = [
            RecruitmentMedia.BIZREACH.value,
            RecruitmentMedia.OPEN_WORK.value,
        ]

        response_media_list = response.data.get('media')
        # レスポンスデータが期待するデータと一致するか確認
        if not response_media_list.sort() == expected_data.sort():
            raise ValueError("Response data is not empty.")

    def test_delete_company_media_invalid_data(self) -> None:
        """
        (異常系) 削除: 媒体IDが存在しない場合
        """
        media_list = [
            RecruitmentMedia.MYNAVI.value,
        ]
        data = {
            "media": media_list
        }

        response = self.client.delete(self.url, data=data, format='json')
        # ステータスコードが400であることを確認
        if not response.status_code == status.HTTP_400_BAD_REQUEST:
            raise ValueError("Status code is not 400.")
