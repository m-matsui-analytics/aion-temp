"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples: # noqa
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dj_rest_auth.views import (
    PasswordChangeView,
)
from django.conf import settings
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

# from api.authentication import UserIDJWTAuthentication
from api import views
from api.views import (
    CandidateView,
    CompanyInfoView,
    CompanyMediaView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    EmpathyEmotionView,
    EmployeeSizeView,
    GenderView,
    IdealCandidateListView,
    IndustryView,
    # JobPostingDetailView,
    JobPostingCreateTextView,
    JobPostingCreateURLView,
    JobPostingView,
    MailGenErrorTypeView,
    MailGenStatusView,
    MailStructureTypeView,
    OccupationView,
    PlanView,
    PositionView,
    PrefectureView,
    RecruitmentArticleCreateTextView,
    RecruitmentArticleCreateURLView,
    RecruitmentArticleView,
    RecruitmentMediaView,
    RequirementLevelView,
)

urlpatterns = [
    # ======================================================== #
    # ================== FOR WEB SERVER URL ================== #
    #----------------------------------------------------------#
    #  ユーザー
    #----------------------------------------------------------#
    # djangorestframework-simplejwt
    path('user/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),


    # # ユーザー情報取得→ユーザー情報はないのでコメントアウト
    # path('user/', UserView.as_view(), name='user-detail'),

    # パスワード変更(dj-rest-auth)  # noqa: ERA001
    path('user/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),  # noqa: E501

    # ユーザー削除

    # 会社概要: 詳細取得、更新、削除
    path('company_info/', CompanyInfoView.as_view(), name='company_info'),


    # 利用媒体: 一覧取得、追加、削除
    path('company_media/', CompanyMediaView.as_view(), name='company_media'),

    # 求める人物像: 一覧取得  # noqa: ERA001
    path('ideal_candidate/', IdealCandidateListView.as_view(), name='ideal_candidate'),


    # 求める人物像: 詳細取得、追加、更新、削除


    #----------------------------------------------------------#
    # 企業の強み
    #----------------------------------------------------------#
    # 企業の強み一覧取得

    # 企業の強み追加

    # 企業の強み更新

    # 企業の強み削除

    #----------------------------------------------------------#
    # 求人票
    #----------------------------------------------------------#
    # 求人票一覧取得
    path("job_posting/", JobPostingView.as_view(), name="job_posting"),

    # 求人票登録（URL)
    path("job_posting/url/", JobPostingCreateURLView.as_view(), name="job_posting_create_url"),

    # 求人票登録（テキスト）
    path("job_posting/text/", views.JobPostingCreateTextView.as_view(), name="job_posting_create_text"),

    # 求人票、詳細取得・更新・削除
    # path("job_posting/<int:id>/", JobPostingDetailView.as_view(), name="job_posting_detail"),

    #----------------------------------------------------------#
    # 採用記事
    #----------------------------------------------------------#
    # 採用記事一覧の取得
    path('recruitment_article/', RecruitmentArticleView.as_view(), name='recruitment_article'),

    # 採用記事登録（URL）
    path('recruitment_article/url/', RecruitmentArticleCreateURLView.as_view(),
        name='recruitment_article_create_url'),

    # 採用記事登録（テキスト）
    path('recruitment_article/text/', RecruitmentArticleCreateTextView.as_view(),
        name='recruitment_article_create_text'),

    # 採用記事、詳細取得・更新・削除

    #----------------------------------------------------------#
    # スカウト送信者
    #----------------------------------------------------------#
    # スカウト送信者一覧取得

    # スカウト送信者追加

    # スカウト送信者更新

    # スカウト送信者削除


    #----------------------------------------------------------#
    # 目標管理
    #----------------------------------------------------------#
    # KPI一覧の取得(年度で絞る)  # noqa: ERA001

    # KPI登録

    # KPI更新

    # KPI削除

    # 達成状況取得

    #----------------------------------------------------------#
    # スカウト
    #----------------------------------------------------------#
    # スカウト一覧の取得

    # スカウト登録 ※候補者を登録したらscoutテーブルとscout_mailテーブルを作成する　10/22追記

    # スカウト更新

    # スカウト削除

    # メール再作成

    # ----------------------------------------------------------#
    # 定数系
    # ----------------------------------------------------------#
    # 従業員数
    path('employee_size/', EmployeeSizeView.as_view(), name='employee_size'),

    # 性別
    path('gender/', GenderView.as_view(), name='gender'),

    # 業種
    path('industry/', IndustryView.as_view(), name='industry'),

    # メール生成エラータイプ
    path('mail_gen_error_type/',MailGenErrorTypeView.as_view(),
        name='mail_gen_error_type'),

    # メール生成ステータス
    path('mail_gen_status/', MailGenStatusView.as_view(), name='mail_gen_status'),

    # メール構成タイプ
    path('mail_structure_type/', MailStructureTypeView.as_view(),
        name='mail_structure_type'),

    # 職種
    path('occupation/', OccupationView.as_view(), name='occupation'),

    # プラン
    path('plan/', PlanView.as_view(), name='plan'),

    # 役職
    path('position/', PositionView.as_view(), name='position'),

    # 都道府県
    path('prefecture/', PrefectureView.as_view(), name='prefecture'),

    # 求める人物像の要求レベル
    path('requirement_level/', RequirementLevelView.as_view(),
        name='requirement_level'),

    # 求人媒体
    path('recruitment_media/', RecruitmentMediaView.as_view(),
        name='recruitment_media'),

    # 共感する感情
    path('empathy_emotion/', EmpathyEmotionView.as_view(),
        name='empathy_emotion'),


    # ======================================================== #
    # ================= FOR GEN SERVERA URL ================== #
    #----------------------------------------------------------#

    path('gen/candidate/', CandidateView.as_view(), name='gen_candidate'),
]

# Debug=Trueの場合、swagger-uiを表示する
if settings.DEBUG:
    urlpatterns += [
        # YOUR PATTERNS
        path('schema/',
            SpectacularAPIView.as_view(
                permission_classes=[AllowAny],
            ),
            name='schema'
        ),
        # Optional UI:
        path(
            'schema/swagger-ui/',
            SpectacularSwaggerView.as_view(
                url_name='schema',
                permission_classes=[AllowAny],
            ),
            name='swagger-ui'
        ),
        path('schema/redoc/',
            SpectacularRedocView.as_view(
                permission_classes=[AllowAny],
            ),
            name='redoc'
        ),
    ]

