# from django.test import TestCase
# from base.models import CompanyInfo, Company, Industry, Prefecture
# from api.serializers import CompanyInfoSerializer

# class CompanyInfoSerializerTestCase(TestCase):
#     def setUp(self):
#         # テスト用の会社を作成
#         self.company = Company.objects.create(
#             name="Test Company"
#         )

#         # テスト用の会社概要情報を作成
#         self.company_info = CompanyInfo.objects.filter(company=self.company).update(
#             foundation_date="2020-01-01",
#             capital="1000000",
#             post_code="1234567",
#             address_prefecture=Prefecture.TOKYO,
#             address_other="Shibuya",
#             ceo_name="John Doe",
#             employee_size=50,
#             business_description="IT Business",
#             industry=Industry.IT_INTERNET,
#             revenue="5000000",
#             mission="Our mission",
#             vision="Our vision",
#             value="Our values"
#         )

#     def test_company_info_serialization(self):
#         """
#         シリアライザが正しくデータをシリアライズすることをテスト
#         """
#         serializer = CompanyInfoSerializer(instance=self.company_info)
#         data = serializer.data

#         # 期待されるデータ
#         expected_data = {
#             'company_name': "Test Company",
#             'foundation_date': "2020-01-01",
#             'capital': "1000000",
#             'post_code': "1234567",
#             'address_prefecture': "Tokyo",
#             'address_other': "Shibuya",
#             'ceo_name': "John Doe",
#             'employee_size': 50,
#             'business_description': "IT Business",
#             'industry': Industry.IT_INTERNET,
#             'revenue': "5000000",
#             'mission': "Our mission",
#             'vision': "Our vision",
#             'value': "Our values",
#         }

#         # データが期待通りかどうかを確認
#         self.assertEqual(data, expected_data)

#     def test_company_info_serialization_with_missing_fields(self):
#         """
#         一部のフィールドが存在しない場合のシリアライザの動作をテスト
#         """
#         self.company_info.address_prefecture = None  # 住所の一部がNoneの場合
#         self.company_info.save()

#         serializer = CompanyInfoSerializer(instance=self.company_info)
#         data = serializer.data

#         # 期待されるデータ
#         expected_data = {
#             'company_name': "Test Company",
#             'foundation_date': "2020-01-01",
#             'capital': "1000000",
#             'post_code': "1234567",
#             'address_prefecture': Prefecture.TOKYO,
#             'address_other': "",
#             'ceo_name': "John Doe",
#             'employee_size': 50,
#             'business_description': "IT Business",
#             'industry': Industry.IT_INTERNET,
#             'revenue': "5000000",
#             'mission': "Our mission",
#             'vision': "Our vision",
#             'value': "Our values",
#         }

#         # データが期待通りかどうかを確認
#         self.assertEqual(data, expected_data)
