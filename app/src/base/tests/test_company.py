from django.test import Client, TestCase
from django.urls import reverse

from base.models import Company, JobPosting

from .utils import create_admin_user, create_superuser, user_login


class AdminCompanyTest(TestCase):
    """
    (テスト) 管理画面でCompanyを論理削除する
    """

    def setUp(self) -> None:
        """
        事前準備
        """
        # 管理画面にアクセスするためのユーザーを作成
        self.client = Client()
        self.user = create_superuser()

        # ログイン
        user_login(self.client, self.user.email, 'test_password')

        # テスト用のCompany（親モデル）とJobPosting（子モデル）を作成  # noqa: RUF003
        self.company = Company.objects.create(name='Test Company')
        self.job_posting = JobPosting.objects.create(
            company=self.company,
            name='Test Job',
            url='https://example.com',
            # media=self.media
        )

    def test_company_soft_delete(self) -> None:
        """
        管理画面でCompanyを論理削除する
        """
        # リクエストを送信
        url = reverse('admin:base_company_delete', args=[self.company.id])
        self.client.post(url, {'post': 'yes'})

        # # Company（親モデル）が論理削除されているか確認  # noqa: RUF003
        self.company.refresh_from_db()
        if not self.company:
            self.fail('Company should not be deleted.')
        if self.company.deleted_at is None:
            self.fail('Company should be set deleted_at.')

        # JobPosting（子モデル）が論理削除されているか確認  # noqa: RUF003
        self.job_posting.refresh_from_db()
        if self.job_posting.deleted_at is None:
            self.fail('JobPosting should be set deleted_at.')

    # def test_job_posting_not_deleted_if_company_not_deleted(self) -> None:
    #     """
    #     Companyを削除せずにJobPostingが削除されないことを確認
    #     """
    #     self.job_posting.refresh_from_db()
    #     if self.job_posting.deleted_at is not None:
    #         self.fail('JobPosting should not be deleted if Company is not deleted.')
