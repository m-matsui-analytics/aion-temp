# """
# ビュー関数のテストモジュール
# """

# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.utils import timezone
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase

# from api.serializers import CompanyInfoSerializer
# from base.models import Company, CompanyInfo, EmployeeSize, Industry, Prefecture

# User = get_user_model()

# class CompanyInfoViewTestCase(APITestCase):
#     """
#     Test case for `CompanyInfoView`.
#     """

#     def setUp(self) -> None:
#         """
#         テスト用のデータのセットアップ
#         """
#         self.company = Company.objects.create(name="Test Company")
#         self.user = User.objects.create_user(
#             email="testuser@test.com",
#             password="testpass123",  # noqa: S106
#             company=self.company
#         )

#         self.company_info = CompanyInfo.objects.filter(company=self.company).first()

#         # 認証用クライアント
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)

#     def test_get_company_info(self) -> None:
#         """
#         会社概要の取得テスト
#         """
#         # GETリクエストの送信
#         url = reverse("company_info")  # `urls.py`で定義された名前を使用
#         response = self.client.get(url)

#         # レスポンスのステータスコードを確認
#         if not response.status_code == status.HTTP_200_OK:
#             raise ValueError("Status code is not 200.")

#         # レスポンスデータを確認
#         serializer_data = CompanyInfoSerializer(instance=self.company_info).data
#         if not response.data == serializer_data:
#             raise ValueError("Response data is not equal to serializer data.")

#     def test_get_company_info_not_found(self) -> None:
#         """
#         会社概要が見つからない場合のテスト
#         """
#         # テストデータを削除して404をテスト
#         self.company_info.deleted_at = timezone.now()
#         self.company_info.save()

#         url = reverse("company_info")
#         response = self.client.get(url)

#         # ステータスコードが404であることを確認
#         if not response.status_code == status.HTTP_404_NOT_FOUND:
#             raise ValueError("Status code is not 404.")


#     def test_update_company_info(self) -> None:
#         """
#         会社概要の更新テスト
#         """
#         url = reverse("company_info")  # `urls.py`で定義された名前を使用
#         data = {
#             "foundation_date": "2022-01-01",
#             "capital": 2000,
#             "post_code": "7654321",
#             "address_prefecture": Prefecture.OSAKA,
#             "address_other": "Updated Address",
#             "ceo_name": "Updated CEO",
#             "employee_size": EmployeeSize._10_TO_99,  # noqa: SLF001
#             "business_description": "Updated Business",
#             "industry": Industry.FINANCE,
#             "revenue": 100000,
#             "mission": "Updated Mission",
#             "vision": "Updated Vision",
#             "value": "Updated Value",
#         }

#         response = self.client.put(url, data, format="json")

#         # レスポンスのステータスコードを確認
#         if not response.status_code == status.HTTP_200_OK:
#             raise ValueError("Status code is not 200.")

#         # 更新後の値を確認
#         self.company_info.refresh_from_db()
#         for field, value in data.items():
#             if getattr(self.company_info, field) != value:
#                 raise ValueError(f"Field '{field}' was not updated correctly.")

#         def test_invalid_post_code(self) -> None:
#             """
#             郵便番号のバリデーションエラーテスト
#             """
#             url = reverse("company_info")
#             data = {"post_code": "1234"}  # 7桁ではないため無効

#             response = self.client.put(url, data, format="json")

#             # レスポンスのステータスコードを確認
#             if not response.status_code == status.HTTP_400_BAD_REQUEST:
#                 raise ValueError("Invalid post code did not raise 400 status code.")

#         def test_invalid_employee_size(self) -> None:
#             """
#             従業員数のバリデーションエラーテスト
#             """
#             url = reverse("company_info")
#             data = {"employee_size": 999}  # 定義されていない従業員数

#             response = self.client.put(url, data, format="json")

#             if not response.status_code == status.HTTP_400_BAD_REQUEST:
#                 raise ValueError("Invalid employee size did not raise 400 status code.")

#         def test_invalid_industry(self) -> None:
#             """
#             業種のバリデーションエラーテスト
#             """
#             url = reverse("company_info")
#             data = {"industry": 999}  # 定義されていない業種

#             response = self.client.put(url, data, format="json")

#             if not response.status_code == status.HTTP_400_BAD_REQUEST:
#                 raise ValueError("Invalid industry did not raise 400 status code.")
