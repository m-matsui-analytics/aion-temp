import uuid
from typing import ClassVar

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from base.models import Company


class CustomUserManager(BaseUserManager):
    """
    カスタムユーザーマネージャー
    """

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: dict
    ) -> "CustomUser":
        """
        一般ユーザー作成
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: dict
    ) -> "CustomUser":
        """
        スーパーユーザー作成
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("account_status", CustomUser.AccountStatus.ACTIVE)
        extra_fields.setdefault("company", Company.objects.get(name="運営会社"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    カスタムユーザーモデル

    | No  | カラム名           | カラム名(日本語)       | データ型       | NULL設定      | 外部キー     | ユニークキー | プログラミング定数     |
    |-----|--------------------|-----------------------|----------------|---------------|--------------|--------------|------------------------|
    | 1   | id                 | ID                    | int            | NOT NULL      |              |              |                        |
    | 2   | email              | メールアドレス        | char(256)      | NOT NULL      |              | 1            |                        |
    | 3   | password           | パスワード            | char(100)      | NOT NULL      |              |              |                        |
    | 4   | account_status     | アカウントステータス  | small_int      | NOT NULL (0)  |              |              | USER_STATUSES          |
    | 5   | company            | 企業ID                | int            | NOT NULL      | companies    |              |                        |
    | 6   | is_staff           | スタッフ              | boolean        | NOT NULL      |              |              |                        |
    | 7   | created_at         | 作成日時              | datetime       | NOT NULL      |              |              |                        |
    | 8   | updated_at         | 更新日時              | datetime       | NOT NULL      |              |              |                        |
    """  # noqa: E501

    class AccountStatus(models.IntegerChoices):
        """
        (定数) アカウントステータス
        """

        TEMPORARY = 0, _("仮登録")
        ACTIVE = 1, _("本登録")
        INACTIVE = 99, _("退会済")

    id = models.UUIDField(
        blank=True,
        null=False,
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        verbose_name="ユーザーID",
    )

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        verbose_name="メールアドレス"
    )

    account_status = models.SmallIntegerField(
        blank=True,
        null=False,
        choices=AccountStatus.choices,
        default=AccountStatus.TEMPORARY,
        verbose_name="アカウントステータス",
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="企業ID",
    )

    is_staff = models.BooleanField(
        blank=True,
        null=False,
        default=False,
        verbose_name="スタッフ"
    )

    is_superuser = models.BooleanField(
        blank=True,
        null=False,
        default=False,
        verbose_name="スーパーユーザー"
    )

    created_at = models.DateTimeField(
        blank=True,
        null=False,
        auto_now_add=True,
        editable=False,
        verbose_name="作成日時",
    )

    updated_at = models.DateTimeField(
        blank=True, null=False, auto_now=True, verbose_name="更新日時"
    )

    history = HistoricalRecords(inherit=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa: RUF012

    objects = CustomUserManager()

    def get_by_natural_key(self, email: str) -> "CustomUser":  # noqa: D102
        return self.get(email=email)

    class Meta:  # noqa: D106
        db_table = "users"
        verbose_name = verbose_name_plural = "ユーザー"
        # constraints: ClassVar = [
        #     models.UniqueConstraint(
        #         fields=["email"],
        #         condition=models.Q(deleted_at=None),
        #         name="unique_email_not_deleted"
        #     )
        # ]

    # def clean(self) -> None:  # noqa: D102
    #     #-----------------------------------------------------------#
    #     # 重複チェック
    #     #-----------------------------------------------------------#
    #     # # email
    #     # if CustomUser.objects.filter(
    #     #         email=self.email,
    #     #     ).exclude(id=self.id).exists():
    #     #     raise ValidationError(_("メールアドレスが重複しています"))

    #     # #-----------------------------------------------------------#
    #     # # 必須項目チェック(on_delete=models.SET_NULLだけど、基本NULL不可の項目)
    #     # #-----------------------------------------------------------#
    #     # if not self.deleted_at:  # noqa: SIM102
    #     #     # company
    #     #     if not self.company:
    #     #         raise ValidationError("Missing required field. [company]")
    #     pass

    # def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
    #     """
    #     保存処理

    #     保存前にバリデーションを実行する
    #     """
    #     self.clean()
    #     super().save(*args, **kwargs)

    # def delete(self, using=None, keep_parents=False) -> None:  # noqa: ANN001, ARG002, FBT002
    #     """
    #     削除処理

    #     物理削除ではなく、deleted_atに削除日時を設定する
    #     """
    #     self.deleted_at = self.updated_at
    #     self.save()

