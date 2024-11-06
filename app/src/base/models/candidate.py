from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .choices import (
    EmpathyEmotion,
    Gender,
    Industry,
    Occupation,
    Position,
    Prefecture,
    RecruitmentMedia,
)


class Candidate(BaseModel):
    """
    候補者モデル

    | カラム名                | カラム名（日本語） | データ型     | NULL設定      | 外部キー            | ユニークキー |
    |-------------------------|--------------------|--------------|--------------|---------------------|--------------|
    | id                      | ID                 | int          | NOT NULL     |                     |              |
    | company_id              | 企業ID             | int          | NOT NULL     | companies           |              |
    | company_candidate_id    | 企業内候補者ID     | int          | NOT NULL     |                     |              |
    | gender                  | 性別               | small_int    | NULL         |                     |              |
    | age                     | 年齢               | small_int    | NULL         |                     |              |
    | address_prefecture      | 居住地（都道府県） | small_int    | NULL         |                     |              |
    | industry                | 業種               | small_int    | NULL         |                     |              |
    | occupation              | 職種               | small_int    | NULL         |                     |              |
    | position                | 役職               | small_int    | NULL         |                     |              |
    | current_company         | 企業名             | varchar(255) | NOT NULL('') |                     |              |
    | department              | 部署名             | varchar(255) | NOT NULL('') |                     |              |
    | job_title               | 役職名             | varchar(255) | NOT NULL('') |                     |              |
    | work_history            | 職務経歴           | text         | NOT NULL('') |                     |              |
    | skill                   | スキル             | text         | NOT NULL('') |                     |              |
    | current_annual_income   | 現在の年収(万円)   | int          | NULL         |                     |              |
    | work_value_1            | 仕事観1            | int          | NULL         | work_values         |              |
    | work_value_2            | 仕事観2            | int          | NULL         | work_values         |              |
    | expectation_1           | 転職に対する期待1  | int          | NULL         | candidates_feelings |              |
    | expectation_2           | 転職に対する期待2  | int          | NULL         | candidates_feelings |              |
    | dissatisfaction_1       | 現職に対する不満1  | int          | NULL         | candidates_feelings |              |
    | dissatisfaction_2       | 現職に対する不満2  | int          | NULL         | candidates_feelings |              |
    | anxiety_1               | 転職に対する不安1  | int          | NULL         | candidates_feelings |              |
    | anxiety_2               | 転職に対する不安2  | int          | NULL         | candidates_feelings |              |
    | is_career_change        | キャリアチェンジ   | boolean      | NULL         |                     |              |
    | ideal_annual_income     | 希望年収(万円)     | int          | NULL         |                     |              |
    | created_at              | 作成日時           | datetime     | NOT NULL     |                     |              |
    | updated_at              | 更新日時           | datetime     | NOT NULL     |                     |              |

    """  # noqa: E501, RUF002

    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="企業"
    )

    # company_candidate_id = models.IntegerField(
    #     blank=False,
    #     null=False,
    #     verbose_name="企業内候補者"
    # )

    media = models.SmallIntegerField(
        blank=False,
        null=False,
        choices=RecruitmentMedia.choices,
        verbose_name="採用媒体"
    )

    id_in_media = models.CharField(
        blank=False,
        null=False,
        default="",
        max_length=255,
        verbose_name="採用媒体内ID"
    )

    last_name = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="姓"
    )

    first_name = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="名"
    )

    gender = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Gender.choices,
        verbose_name="性別"
    )

    age = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name="年齢"
    )

    prefecture = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Prefecture.choices,
        verbose_name="居住地（都道府県）"  # noqa: RUF001
    )

    industry = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Industry.choices,
        verbose_name="業種"
    )

    occupation = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Occupation.choices,
        verbose_name="職種"
    )

    position = models.SmallIntegerField(
        blank=True,
        null=True,
        choices=Position.choices,
        verbose_name="役職"
    )

    current_company = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="企業名"
    )

    department = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="部署名"
    )

    job_title = models.CharField(
        blank=True,
        null=False,
        default="",
        max_length=255,
        verbose_name="役職名"
    )

    current_annual_income_min = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="現年収の下限(万円)"
    )

    current_annual_income_max = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="現年収の上限(万円)"
    )

    work_value_1 = models.ForeignKey(
        "WorkValue",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="c_work_value_1",
        verbose_name="仕事観1"
    )

    work_value_2 = models.ForeignKey(
        "WorkValue",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="c_work_value_2",
        verbose_name="仕事観2"
    )

    expectation_1 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="expectation_1",
        verbose_name="転職に対する期待1"
    )

    expectation_2 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="expectation_2",
        verbose_name="転職に対する期待2"
    )

    dissatisfaction_1 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dissatisfaction_1",
        verbose_name="現職に対する不満1"
    )

    dissatisfaction_2 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="dissatisfaction_2",
        verbose_name="現職に対する不満2"
    )

    anxiety_1 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="anxiety_1",
        verbose_name="転職に対する不安1"
    )

    anxiety_2 = models.ForeignKey(
        "CandidateFeeling",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="anxiety_2",
        verbose_name="転職に対する不安2"
    )

    is_career_change = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="キャリアチェンジ"
    )

    preferred_annual_income = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="希望年収(万円)"
    )

    labels = models.ManyToManyField(
        "Label",
        through="CandidateLabel",
        verbose_name="ラベル"
    )

    class Meta:  # noqa: D106
        db_table = "candidates"
        verbose_name = verbose_name_plural = "<< 候補者 >>"
        app_label = 'base'

    def __str__(self) -> str:  # noqa: D105
        if self.last_name or self.first_name:
            return f"{self.last_name} {self.first_name}"
        return f"{self.id_in_media}"


    def clean(self) -> None:  # noqa: D102
        #-----------------------------------------------------------#
        # expectation_1, expectation_2
        #-----------------------------------------------------------#

        # expectation_1とexpectation_2が同じ値ではないかチェック
        if self.expectation_1 and self.expectation_2 \
            and self.expectation_1 == self.expectation_2:
            raise ValidationError("Invalid value. [expectation_1, expectation_2]")

        # expectation_1とexpectation_2の値がCandidateFeelingのemotion_type=EXPECTATIONかチェック  # noqa: E501, ERA001
            if self.expectation_1 and self.expectation_1.emotion_type != \
                EmpathyEmotion.EXPECTATION:
                raise ValidationError("Invalid value. [expectation_1]")
            if self.expectation_2 and self.expectation_2.emotion_type != \
                EmpathyEmotion.EXPECTATION:
                raise ValidationError("Invalid value. [expectation_2]")

        #-----------------------------------------------------------#
        # dissatisfaction_1, dissatisfaction_2
        #-----------------------------------------------------------#

        # dissatisfaction_1とdissatisfaction_2が同じ値の場合はエラーを返す
        if self.dissatisfaction_1 and self.dissatisfaction_2 \
            and self.dissatisfaction_1 == self.dissatisfaction_2:
            raise ValidationError("Invalid value. [dissatisfaction_1, dissatisfaction_2]")  # noqa: E501

        # dissatisfaction_1とdissatisfaction_2の値がCandidateFeelingのemotion_type=DISSATISFACTIONでない場合はエラーを返す  # noqa: E501, ERA001
        if self.dissatisfaction_1 and self.dissatisfaction_1.emotion_type != \
            EmpathyEmotion.DISSATISFACTION:
            raise ValidationError("Invalid value. [dissatisfaction_1]")
        if self.dissatisfaction_2 and self.dissatisfaction_2.emotion_type != \
            EmpathyEmotion.DISSATISFACTION:
            raise ValidationError("Invalid value. [dissatisfaction_2]")


        #-----------------------------------------------------------#
        # anxiety_1, anxiety_2
        #-----------------------------------------------------------#
        # anxiety_1とanxiety_2が同じ値の場合はエラーを返す
        if self.anxiety_1 and self.anxiety_2 \
            and self.anxiety_1 == self.anxiety_2:
                raise ValidationError("Invalid value. [anxiety_1, anxiety_2]")

        # anxiety_1とanxiety_2の値がCandidateFeelingのemotion_type=ANXIETYでない場合はエラーを返す  # noqa: E501, ERA001
        if self.anxiety_1 and self.anxiety_1.emotion_type != EmpathyEmotion.ANXIETY:
            raise ValidationError("Invalid value. [anxiety_1]")
        if self.anxiety_2 and self.anxiety_2.emotion_type != EmpathyEmotion.ANXIETY:
            raise ValidationError("Invalid value. [anxiety_2]")


    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """作成・追加時の前処理を追加"""
        self.full_clean()
        super().save(*args, **kwargs)
