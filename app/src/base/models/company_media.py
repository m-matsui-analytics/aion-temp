from typing import ClassVar

from django.db import models

from .base import BaseModel
from .choices import RecruitmentMedia


class CompanyMedia(BaseModel):
    """
    企業の利用媒体モデル

    | カラム名      | カラム名（日本語）  | データ型    | NULL設定   | 外部キー           | ユニークキー |
    |---------------|--------------------|-------------|------------|--------------------|--------------|
    | id            | ID                 | int         | NOT NULL   |                    |              |
    | company_id    | 企業ID             | int         | NOT NULL   | companies          |              |
    | media         | 媒体ID             | int         | NOT NULL   | recruitment_medias |              |
    | created_at    | 作成日時           | datetime    | NOT NULL   |                    |              |
    | updated_at    | 更新日時           | datetime    | NOT NULL   |                    |              |

    複合キー:
    | 名称           | カラム                      |
    |----------------|-----------------------------|
    | company_media  | ・company_id<br>・media_id  |

    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業"
    )

    media = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=RecruitmentMedia.choices,
        verbose_name="採用媒体"
    )


    class Meta: # noqa: D106
        db_table = "company_medias"
        verbose_name = verbose_name_plural = "利用している採用媒体"
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["company", "media"],
                name="company_media"
            )
        ]
        app_label = "base"

    def __str__(self) -> str: # noqa: D105
        return f"{self.company.name} {self.get_media_display()}"
