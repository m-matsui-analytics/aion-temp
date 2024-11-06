import os

from base.models.choices import RelevanceLevel
from base.models.company_strength import CompanyStrength
from base.models.company_strength_jp import CompanyStrengthJP
from base.models.company_strength_ra import CompanyStrengthRA
from base.models.ideal_candidate import IdealCandidate
from base.models.ideal_candidate_jp import IdealCandidateJP
from base.models.ideal_candidate_ra import IdealCandidateRA
from base.models.job_posting import JobPosting
from base.models.recruitment_article import RecruitmentArticle


TARGET_TYPE_JOB_POSTING = int(os.getenv("TARGET_TYPE_JOB_POSTING"))
TARGET_TYPE_RECRUITMENT_ARTICLE = int(os.getenv("TARGET_TYPE_RECRUITMENT_ARTICLE"))

class ContentAnalysisUpdater():
    """
    コンテンツの解析結果を更新するタスク

    コンテンツの解析結果を受け取り、DBに保存する
    更新するモデル一覧
    - CompanyStrengthJP
    - CompanyStrengthRA
    - IdealCandidateJP
    - IdealCandidateRA
    - JobPosting
    - RecruitmentArticle
    """

    def __init__(
            self,
            company_id: int,
            target_type: str,
            content_id: int,
            content_analysis_log_id: int,
            result: dict,
        ) -> None:
        """
        コンストラクタ

        Args:
        ----
        company_id (int): 企業ID
        target_type (str): ターゲットタイプ
        content_id (int): コンテンツID
        content_analysis_log_id (int): コンテンツ解析ログID
        result (dict): 解析結果

        """
        self.company_id = company_id
        self.target_type = target_type
        self.content_id = content_id
        self.content_analysis_log_id = content_analysis_log_id
        self.result = result

    def update(self) -> None:
        """
        コンテンツの解析結果を更新する
        """
        print("Update ContentAnalysis")
        if self.target_type == TARGET_TYPE_JOB_POSTING:
            self.__update_job_posting()
        elif self.target_type == TARGET_TYPE_RECRUITMENT_ARTICLE:
            self.__update_recruitment_article()

    def __update_job_posting(self) -> None:
        """
        求人記事の解析結果を更新する
        """
        print("Update JobPosting")
        # 求人記事の解析結果を更新
        job_posting = JobPosting.objects.get(pk=self.content_id)
        job_posting.summary = self.result.get("summary")
        job_posting.save()

        # 求める人物像 - 求人票を更新
        # 既存のデータを削除
        IdealCandidateJP.objects.filter(job_posting_id=self.content_id).delete()
        # 新規データを追加
        for ic_id in self.result.get("ideal_candidate_id_list"):
            IdealCandidateJP.objects.create(
                job_posting=job_posting,
                ideal_candidate=IdealCandidate.objects.get(pk=ic_id["id"]),
                relevance_level=ic_id["relevance_level_id"],
            )

        # 企業の強み - 求人票を更新
        # 既存のデータを削除
        CompanyStrengthJP.objects.filter(job_posting_id=self.content_id).delete()
        # 新規データを追加
        for strength_id in self.result.get("strength_id_list"):
            CompanyStrengthJP.objects.create(
                job_posting=job_posting,
                strength=CompanyStrength.objects.get(pk=strength_id["id"]),
                relevance_level=strength_id["relevance_level_id"],
            )

    def __update_recruitment_article(self) -> None:
        """
        採用記事の解析結果を更新する
        """
        print("Update RecruitmentArticle")
        # 採用記事の解析結果を更新
        recruitment_article = RecruitmentArticle.objects.get(id=self.content_id)
        recruitment_article.summary = self.result.get("summary")
        recruitment_article.save()

        # 求める人物像 - 採用記事を更新
        # 既存のデータを削除
        IdealCandidateRA.objects.filter(recruitment_article_id=self.content_id).delete()
        # 新規データを追加
        for ic_id in self.result.get("ideal_candidate_id_list"):
            IdealCandidateRA.objects.create(
                recruitment_article=recruitment_article,
                ideal_candidate=IdealCandidate.objects.get(pk=ic_id["id"]),
                relevance_level=ic_id["relevance_level_id"],
            )

        # 企業の強み - 採用記事を更新
        # 既存のデータを削除
        CompanyStrengthRA.objects.filter(recruitment_article_id=self.content_id).delete()
        # 新規データを追加
        for strength_id in self.result.get("strength_id_list"):
            CompanyStrengthRA.objects.create(
                recruitment_article=recruitment_article,
                strength=CompanyStrength.objects.get(pk=strength_id["id"]),
                relevance_level=strength_id["relevance_level_id"],
            )

    def validate(self) -> None:
        """
        コンテンツの解析結果のバリデーション
        """
        print("Validate ContentAnalysisUpdater")
        ###############################################################
        # summary
        ###############################################################
        # summaryが存在しない場合
        if not self.result.get("summary"):
            raise ValueError("summary not found")

        ###############################################################
        # ideal_candidate_id_list(存在する場合)
        ###############################################################
        if self.result.get("ideal_candidate_id_list"):
            self.__validate_ideal_candidate_id_list()

        ###############################################################
        # strength_id_list(存在する場合)
        ###############################################################
        if self.result.get("strength_id_list"):
            self.__validate_strength_id_list()

    def __validate_ideal_candidate_id_list(self) -> None:
        """
        理想の候補者IDリストのバリデーション
        """
        print("Validate ideal_candidate_id_list")
        ic_id_list = self.result.get("ideal_candidate_id_list")
        # リスト型でなければエラー
        if not isinstance(ic_id_list, list):
            raise TypeError("ideal_candidate_id_list is not list")

        # 各要素に対してバリデーション
        for ic_id in ic_id_list:
            # idというキーが存在しない場合はエラー
            if not ic_id.get("id"):
                raise ValueError("ideal_candidate_id not found")

            # idが存在しない場合はエラー
            if not IdealCandidate.objects.filter(id=ic_id["id"]).exists():
                err_msg = f"ideal_candidate_id is invalid. value: {ic_id['id']}"
                raise ValueError(err_msg)

            # relevance_level_idキーが存在しない場合はエラー
            if not ic_id.get("relevance_level_id"):
                raise ValueError("relevance_level_id not found")

            # relevance_level_idが存在しない場合はエラー
            if ic_id["relevance_level_id"] not in RelevanceLevel.values:
                err_msg = f"relevance_level_id is invalid. value: {ic_id['relevance_level_id']}"
                raise ValueError(err_msg)

    def __validate_strength_id_list(self) -> None:
        """
        強みIDリストのバリデーション
        """
        print("Validate strength_id_list")
        strength_id_list = self.result.get("strength_id_list")
        # リスト型でなければエラー
        if not isinstance(strength_id_list, list):
            raise TypeError("strength_id_list is not list")

        # 各要素に対してバリデーション
        for strength_id in self.result.get("strength_id_list"):
            # idというキーが存在しない場合はエラー
            if not strength_id.get("id"):
                raise ValueError("strength_id not found")

            # idが存在しない場合はエラー
            if not CompanyStrength.objects.filter(id=strength_id["id"]).exists():
                err_msg = f"strength_id is invalid. value: {strength_id['id']}"
                raise ValueError(err_msg)

            # relevance_level_idキーが存在しない場合はエラー
            if not strength_id.get("relevance_level_id"):
                raise ValueError("relevance_level_id not found")

            # relevance_level_idが存在しない場合はエラー
            if strength_id["relevance_level_id"] not in RelevanceLevel.values:
                err_msg = f"relevance_level_id is invalid. value: {strength_id['relevance_level_id']}"
                raise ValueError(err_msg)

