from django.core.validators import RegexValidator
from django.db import models

from .base import BaseModel
from .choices import EmployeeSize, Industry, Prefecture


class CompanyInfo(BaseModel):
    """
    会社概要モデル

    | カラム名                    | カラム名(日本語)     | データ型        | NULL設定     | 外部キー      | ユニークキー | プログラミング定数 | 入力経路 |
    |-----------------------------|---------------------|-----------------|--------------|---------------|--------------|--------------------|----------|
    | id                          | ID                  | int             | NOT NULL     |               |              |                    | システム   |
    | company_id                  | 企業ID              | int             | NOT NULL     | companies     |              |                    | システム   |
    | foundation_date             | 設立日              | date            | NULL         |               |              |                    | ユーザー   |
    | capital                     | 資本金              | int             | NULL         |               |              |                    | ユーザー   |
    | post_code                   | 郵便番号            | int             | NULL         |               |              |                    | ユーザー   |
    | address_prefecture_id       | 県ID                | small_int       | NULL         |               |              | PREFECTURES        | ユーザー   |
    | address_other               | 住所(県以下)        | varchar(200)    | NOT NULL('') |               |              |                    | ユーザー   |
    | ceo_name                    | 代表者名            | varchar(100)    | NOT NULL('') |               |              |                    | ユーザー   |
    | employee_size               | 従業員数            | int             | NULL         |               |              | EMPLOYEE_SIZES     | ユーザー   |
    | business_description        | 事業内容            | varchar(200)    | NOT NULL('') |               |              |                    | ユーザー   |
    | industry                    | 業種                | small_int       | NULL         |               |              | INDUSTRIES         | ユーザー   |
    | revenue                     | 売上高              | int             | NULL         |               |              |                    | ユーザー   |
    | mission                     | ミッション          | text            | NOT NULL('') |               |              |                    | ユーザー   |
    | vision                      | ビジョン            | text            | NOT NULL('') |               |              |                    | ユーザー   |
    | value                       | バリュー            | text            | NOT NULL('') |               |              |                    | ユーザー   |
    | created_at                  | 作成日時            | datetime        | NOT NULL     |               |              |                    | システム   |
    | updated_at                  | 更新日時            | datetime        | NOT NULL     |               |              |                    | システム   |
    | deleted_at                  | 削除日時            | datetime        | NULL         |               |              |                    | システム   |

    """  # noqa: E501

    # Validator----------------------------------------
    postal_code_regex = RegexValidator(
        regex=r'^[0-9]{7}$',
        message = ("Invalid")
    )
    # -------------------------------------------------


    company = models.OneToOneField(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業ID"
    )

    foundation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="設立日"
    )

    capital = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="資本金(千円)"
    )

    post_code = models.IntegerField(
        blank=True,
        null=True,
        validators=[postal_code_regex],
        verbose_name="郵便番号"
    )

    address_prefecture = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Prefecture.choices,
        verbose_name="所在地(都道府県)"
    )

    address_other = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="所在地(県以下)"
    )

    ceo_name = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=100,
        verbose_name="代表者名"
    )

    employee_size = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=EmployeeSize.choices,
        verbose_name="従業員数"
    )

    business_description = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="事業内容"
    )

    industry = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Industry.choices,
        verbose_name="業種"
    )

    revenue = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="売上高(百万円)"
    )

    mission = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="ミッション"
    )

    vision = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="ビジョン"
    )

    value = models.TextField(
        blank=True,
        null=False,
        default="",
        verbose_name="バリュー"
    )


    class Meta:  # noqa: D106
        db_table = "company_info"
        verbose_name = verbose_name_plural = "会社概要"
        app_label = "base"

    def __str__(self) -> str:  # noqa: D105
        return self.company.name
