"""
Modelの選択肢を定義するモジュール

※変更したら必ず下記システムの定数を変更する
* メール生成機能(/mail_gen)
* コンテンツ解析機能(/content_analysis)
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Education(models.IntegerChoices):
    """
    (選択肢) 学歴

    | 選択肢         | 選択肢(日本語)    | 値  |
    |----------------|-------------------|-----|
    | DOCTOR         | 大学院卒（博士）  | 1   |
    | MASTER         | 大学院卒（修士）  | 2   |
    | UNIVERSITY     | 大学卒            | 3   |
    | JUNIOR_COLLEGE | 高専・専門・短大卒 | 4   |
    | HIGH_SCHOOL    | 高校卒            | 5   |
    """ # noqa: RUF002

    DOCTOR = 1, _("大学院（博士）卒") # noqa: RUF001
    MASTER = 2, _("大学院（修士）卒") # noqa: RUF001
    UNIVERSITY = 3, _("大学卒")
    JUNIOR_COLLEGE = 4, _("高専・専門・短大卒")
    HIGH_SCHOOL = 5, _("高校卒")


class EmpathyEmotion(models.IntegerChoices):
    """
    (選択肢) 共感する感情

    | 選択肢              | 選択肢(日本語)        | 値  |
    |---------------------|-----------------------|-----|
    | EXPECTATION         | 転職に対する期待      | 1   |
    | DISSATISFACTION     | 現職に対する不満      | 2   |
    | ANXIETY             | 転職に対する不安      | 3   |
    """

    EXPECTATION = 1, _("転職に対する期待")
    DISSATISFACTION = 2, _("現職に対する不満")
    ANXIETY = 3, _("転職に対する不安")


class EmployeeSize(models.IntegerChoices):
    """
    (選択肢) 従業員数

    | 選択肢             | 選択肢(日本語)       | 値  |
    |--------------------|----------------------|-----|
    | LESS_THAN_10       | 10人以下             | 1   |
    | 10_TO_99           | 10～99人             | 2   |
    | 100_TO_999         | 100～999人           | 3   |
    | 1000_AND_ABOVE     | 1000人以上           | 4   |
    """  # noqa: RUF002

    LESS_THAN_10 = 1, _("10人以下")
    _10_TO_99 = 2, _("10～99人")  # noqa: RUF001
    _100_TO_999 = 3, _("100～999人")  # noqa: RUF001
    _1000_AND_ABOVE = 4, _("1000人以上")


class EmploymentStatus(models.IntegerChoices):
    """
    (選択肢) 就業状況

    | 選択肢             | 選択肢(日本語) | 値 |
    |--------------------|----------------|----|
    | CURRENT            | 現職           | 1  |
    | RESIGNED_3_MONTH   | 離職3ヶ月以内  | 2  |
    | RESIGNED_6_MONTH   | 離職半年以内   | 3  |
    | RESIGNED_1_YEAR    | 離職1年以内    | 4  |
    """

    CURRENT = 1, _("現職")
    RESIGNED_3_MONTH = 2, _("離職3ヶ月以内")
    RESIGNED_6_MONTH = 3, _("離職半年以内")
    RESIGNED_1_YEAR = 4, _("離職1年以内")


class Gender(models.IntegerChoices):
    """
    (選択肢) 性別

    | 選択肢        | 選択肢（日本語）     | 値  |
    |---------------|----------------------|-----|
    | MALE          | 男性                 | 1   |
    | FEMALE        | 女性                 | 2   |
    | UNSPECIFIED   | 未選択               | 99  | ←"不明"だと印象が悪い為、未選択とした
    """ # noqa: RUF002

    MALE = 1, _("男性")
    FEMALE = 2, _("女性")
    UNSPECIFIED = 99, _("未選択")


class HTMLContentAnalysisErrorType(models.IntegerChoices):
    """
    (選択肢) HTMLコンテンツ解析エラータイプ

    | 選択肢                    | 選択肢(日本語)    | 値  |
    |---------------------------|-------------------|-----|
    | HTML_FETCH_FAILURE        | HTML取得失敗エラー    | 1   |
    | ELEMENT_RETRIEVAL_FAILURE | 要素取得エラー        | 2   |
    | LLM_ANALYSIS_FAILURE      | LLMによる解析エラー   | 3   |
    | SYSTEM_ERROR              | システムエラー        | 99   |
    """

    HTML_FETCH_FAILURE = 1, _("HTML取得失敗エラー")
    ELEMENT_RETRIEVAL_FAILURE = 2, _("要素取得エラー")
    LLM_ANALYSIS_FAILURE = 3, _("LLMによる解析エラー")
    SYSTEM_ERROR = 99, _("システムエラー")


class HTMLContentAnalysisStatus(models.IntegerChoices):
    """
    (選択肢) HTMLコンテンツ解析ステータス

    | 選択肢        | 選択肢(日本語)     | 値  |
    |---------------|--------------------|-----|
    | IN_PROGRESS   | 登録中             | 1   |
    | SUCCESS       | 成功               | 2   |
    | FAILURE       | 失敗               | 3   |
    """

    IN_PROGRESS = 1, _("登録中")
    SUCCESS = 2, _("成功")
    FAILURE = 3, _("失敗")


class HTMLContentAnalysisProcess(models.IntegerChoices):
    """
    (選択肢) HTMLコンテンツ解析プロセス

    ※数字3桁。先頭の番号がステップを示し、下2桁がプロセスを示す。

    ## ステップ一覧
    | No  | ステップ名                  | 役割           |
    | --- | --------------------------- | -------------- |
    | 1   | [STEP_ELEMENT_RETRIEVAL](#) | HTML要素の取得 |
    | 2   | [STEP_ANALYSIS](#)          | 解析           |
    | 3   | [STEP_LOGGING](#)           | ログの記録     |


    ## プロセス一覧
    ### STEP_ELEMENT_RETRIEVAL
    | ID  | プロセス名               | 役割           |
    | --- | ------------------------ | -------------- |
    | 110 | FETCH_HTML       | HTMLの取得     |
    | 120 | RETRIEVE_ELEMENT | HTML要素の取得 |


    ### STEP_ANALYSIS
    | ID  | プロセス名                     | 役割                           |
    | --- | ------------------------------ | ------------------------------ |
    | 210 | SELECT_IDEAL_CANDIDATE | 関連する求める人物像を選択する         |
    | 220 | SELECT_STRENGTH        | 関連する企業の強みを選択する |


    ### STEP_LOGGING
    | ID  | プロセス名                 | 役割               |
    | --- | -------------------------- | ------------------ |
    | 310 | RECORD_SUCCESS_LOG | 成功ログを記録する |
    | 320 | RECORD_FAILURE_LOG | 失敗ログを記録する |
    """

    FETCH_HTML = 110, _("HTMLの取得")
    RETRIEVE_ELEMENT = 120, _("HTML要素の取得")
    SELECT_IDEAL_CANDIDATE = 210, _("求める人物像を選択する")
    SELECT_STRENGTH = 220, _("関連のある企業の強みを選択する")
    RECORD_SUCCESS_LOG = 310, _("成功ログを記録する")
    RECORD_FAILURE_LOG = 320, _("失敗ログを記録する")


class Industry(models.IntegerChoices):
    """
    (選択肢) 業種

    | 選択肢                        | 選択肢 （日本語）               | 値  |
    |-------------------------------|---------------------------------|-----|
    | IT_INTERNET                   | IT・インターネット              | 1   |
    | MANUFACTURER                  | メーカー                        | 2   |
    | TRADING_COMPANY               | 商社                            | 3   |
    | RETAIL                        | 流通・小売                      | 4   |
    | CONSULTING                    | コンサルティング                | 5   |
    | MASS_MEDIA                    | マスコミ・メディア              | 6   |
    | ENTERTAINMENT                 | エンターテインメント            | 7   |
    | FINANCE                       | 金融                            | 8   |
    | CONSTRUCTION                  | 建設                            | 9   |
    | MEDICAL                       | メディカル                      | 10  |
    | ENERGY                        | エネルギー                      | 11  |
    | INSURANCE                     | 保険                            | 12  |
    | REAL_ESTATE                   | 不動産                          | 13  |
    | LEGAL_PROFESSION              | 士業                            | 14  |
    | SERVICE_INDUSTRY              | サービス                        | 15  |
    | TRANSPORTATION                | 運輸・交通                      | 16  |
    | LOGISTICS_WAREHOUSE           | 物流・倉庫                      | 17  |
    | OTHER_EDUCATION_GOVERNMENT    | その他（教育・官公庁）など       | 99  |
    """  # noqa: RUF002

    IT_INTERNET = 1, _("IT・インターネット")
    MANUFACTURER = 2, _("メーカー")
    TRADING_COMPANY = 3, _("商社")
    RETAIL = 4, _("流通・小売")
    CONSULTING = 5, _("コンサルティング")
    MASS_MEDIA = 6, _("マスコミ・メディア")
    ENTERTAINMENT = 7, _("エンターテインメント")
    FINANCE = 8, _("金融")
    CONSTRUCTION = 9, _("建設")
    MEDICAL = 10, _("メディカル")
    ENERGY = 11, _("エネルギー")
    INSURANCE = 12, _("保険")
    REAL_ESTATE = 13, _("不動産")
    LEGAL_PROFESSION = 14, _("士業")
    SERVICE_INDUSTRY = 15, _("サービス")
    TRANSPORTATION = 16, _("運輸・交通")
    LOGISTICS_WAREHOUSE = 17, _("物流・倉庫")
    OTHER_EDUCATION_GOVERNMENT = 99, _("その他（教育・官公庁）など") # noqa: RUF001

class MailGenErrorType(models.IntegerChoices):
    """
    (選択肢) メール生成エラータイプ

    | 選択肢                    | 選択肢(日本語)    | 値  |
    |---------------------------|-------------------|-----|
    | INSUFFICIENT_INFORMATION  | 情報不足エラー    | 1   |
    | VERIFY_IDEAL_CANDIDATE_MATCH | マッチングエラー  | 2   |
    | INSUFFICIENT_APPEAL_POINT | 訴求ポイント不足エラー  | 3   |
    | SYSTEM                    | システムエラー    | 99   |
    """

    INSUFFICIENT_INFORMATION = 1, _("情報不足エラー")
    VERIFY_IDEAL_CANDIDATE_MATCH = 2, _("マッチングエラー")
    INSUFFICIENT_APPEAL_POINT = 3, _("訴求ポイント不足エラー")
    SYSTEM = 99, _("システムエラー")


class MailGenStatus(models.IntegerChoices):
    """
    (選択肢) メール生成ステータス

    | 選択肢        | 選択肢(日本語)     | 値  |
    |---------------|--------------------|-----|
    | IN_PROGRESS   | 作成中             | 1   |
    | SUCCESS       | 成功               | 2   |
    | FAILURE       | 失敗               | 3   |
    """

    IN_PROGRESS = 1, _("作成中")
    SUCCESS = 2, _("成功")
    FAILURE = 3, _("失敗")


class MailGenProcess(models.IntegerChoices):
    """
    (選択肢) メール生成プロセス

    ※数字3桁。先頭の番号がステップを示し、下2桁がプロセスを示す。

    ## ステップ一覧
    | No | ステップ名 | 役割 |
    |---|------------|------|
    | 1 | [STEP_EXTRACT_CANDIDATE_INFO](#extract_candidate_info) | 候補者情報の抽出 |
    | 2 | [STEP_MATCHING](#matching) | マッチング |
    | 3 | [STEP_GENERATE_MAIL](#generate_mail) | メール生成 |

    ## STEP_EXTRACT_CANDIDATE_INFO
    | 選択肢        | 選択肢(日本語)     | 値  |
    |---------------|--------------------|-----|
    | EXTRACT_CANDIDATE_PROFILE  | 候補者プロフィールの抽出 | 100  |
    | EXTRACT_CAREER_DETAIL| 候補者のキャリア情報の抽出 | 200   |

    ## STEP_MATCHING
    | 選択肢        | 選択肢(日本語)     | 値  |
    | VERIFY_IDEAL_CANDIDATE_MATCH | 候補者が企業の求める人物像に適合するか判定| 100  |

    ## STEP_GENERATE_MAIL
    | 選択肢        | 選択肢(日本語)     | 値  |
    | SELECT_EMPATHY_EMOTION | 共感する感情を選択する | 100  |
    | SELECT_APPEAL_POINT |  訴求する強みを選択する | 200  |
    | SELECT_JOB_POSTING | 添付する求人情報を選択する | 300  |
    | SELECT_RECRUITMENT_CONTENT | 添付する採用記事を選択する | 400  |
    | SELECT_MAIL_STRUCTURE | メール構成を選択する | 500  |
    | SELECT_SENDER | 差出人を選択する | 600  |
    | GENERATE_SUBJECT | タイトルを生成する | 700  |
    | GENERATE_BODY | 本文を生成する | 800  |
    """

    EXTRACT_CANDIDATE_PROFILE = 110, _("候補者プロフィールの抽出")
    EXTRACT_CAREER_DETAIL = 120, _("候補者のキャリア情報の抽出")
    VERIFY_IDEAL_CANDIDATE_MATCH = 210, _("候補者が企業の求める人物像に適合するか判定")
    SELECT_EMPATHY_EMOTION = 310, _("共感する感情を選択する")
    SELECT_MAIL_STRUCTURE = 320, _("メール構成を選択する")
    SELECT_APPEAL_POINT = 330, _("訴求する強みを選択する")
    SELECT_JOB_POSTING = 340, _("添付する求人情報を選択する")
    SELECT_RECRUITMENT_CONTENT = 350, _("添付する採用記事を選択する")
    SELECT_SENDER = 360, _("差出人を選択する")
    GENERATE_SUBJECT = 370, _("タイトルを生成する")
    GENERATE_BODY = 380, _("本文を生成する")


class MailStructureType(models.IntegerChoices):
    """
    (選択肢) メール構成タイプ

    | 選択肢                | 選択肢(日本語)      | 値  |
    |-----------------------|---------------------|-----|
    | EXPECTATION_TYPE      | 期待向上型          | 1   |
    | RELIEF_TYPE           | 不満・不安解消型    | 2   |
    """

    EXPECTATION_TYPE = 1, _("期待向上型")
    RELIEF_TYPE = 2, _("不満・不安解消型")


class Occupation(models.IntegerChoices):
    """
    (選択肢) 職種

    | 選択肢                           | 選択肢(日本語)                  | 値  |
    |----------------------------------|---------------------------------|-----|
    | EXECUTIVE                        | 経営                            | 1   |
    | ADMINISTRATION                   | 管理                            | 2   |
    | MARKETING                        | マーケティング                  | 3   |
    | SALES                            | 営業                            | 4   |
    | CONSULTANT                       | コンサルタント                  | 5   |
    | IT_CONSULTANT                    | ITコンサルタント                | 6   |
    | SPECIALIST                       | 専門職                          | 7   |
    | IT_ENGINEERING                   | IT技術職                        | 8   |
    | GAME                             | ゲーム                          | 9   |
    | ELECTRICAL_ELECTRONIC            | 電気・電子                      | 10  |
    | SEMICONDUCTOR                    | 半導体                          | 11  |
    | MACHINERY                        | 機械                            | 12  |
    | CHEMISTRY                        | 化学                            | 13  |
    | FINANCE                          | 金融                            | 14  |
    | RESEARCH_CLINICAL_DEVELOPMENT    | 研究・臨床開発・治験            | 15  |
    | ARCHITECTURE_CIVIL_ENGINEERING   | 建築・土木                      | 16  |
    | HUMAN_RESOURCES                  | 人事                            | 17  |
    | SERVICE                          | サービス                        | 18  |
    | PROJECT_MANAGEMENT               | プロジェクト管理                | 19  |
    | WEB_SERVICE_CREATION             | Webサービス・制作               | 20  |
    | DIGITAL_MARKETING                | デジタルマーケティング          | 21  |
    | ADVERTISEMENT                    | 広告                            | 22  |
    | NEWSPAPER_PUBLISHING             | 新聞・出版                      | 23  |
    | TV_BROADCASTING_FILM_SOUND       | テレビ・放送・映像・音響        | 24  |
    | DESIGN                           | デザイン                        | 25  |
    | MATERIAL                         | 素材                            | 26  |
    | FOOD                             | 食品                            | 27  |
    | COSMETICS                        | 化粧品                          | 28  |
    | DAILY_GOODS                      | 日用品                          | 29  |
    | REAL_ESTATE                      | 不動産                          | 30  |
    | CONSTRUCTION_MANAGEMENT          | 施工管理                        | 31  |
    | MEDICAL_SALES                    | 医療営業                        | 32  |
    | PRODUCTION_QUALITY_MANAGEMENT    | 生産管理・品質管理・品質保証    | 33  |
    | ACADEMIC_PMS_REGULATORY          | 学術・PMS・薬事                 | 34  |
    | MEDICAL_NURSING_PHARMACY         | 医療・看護・薬剤                | 35  |
    | UNKNOWN                          | 不明                            | 99  |
    """

    EXECUTIVE = 1, _("経営")
    ADMINISTRATION = 2, _("管理")
    MARKETING = 3, _("マーケティング")
    SALES = 4, _("営業")
    CONSULTANT = 5, _("コンサルタント")
    IT_CONSULTANT = 6, _("ITコンサルタント")
    SPECIALIST = 7, _("専門職")
    IT_ENGINEERING = 8, _("IT技術職")
    GAME = 9, _("ゲーム")
    ELECTRICAL_ELECTRONIC = 10, _("電気・電子")
    SEMICONDUCTOR = 11, _("半導体")
    MACHINERY = 12, _("機械")
    CHEMISTRY = 13, _("化学")
    FINANCE = 14, _("金融")
    RESEARCH_CLINICAL_DEVELOPMENT = 15, _("研究・臨床開発・治験")
    ARCHITECTURE_CIVIL_ENGINEERING = 16, _("建築・土木")
    HUMAN_RESOURCES = 17, _("人事")
    SERVICE = 18, _("サービス")
    PROJECT_MANAGEMENT = 19, _("プロジェクト管理")
    WEB_SERVICE_CREATION = 20, _("Webサービス・制作")
    DIGITAL_MARKETING = 21, _("デジタルマーケティング")
    ADVERTISEMENT = 22, _("広告")
    NEWSPAPER_PUBLISHING = 23, _("新聞・出版")
    TV_BROADCASTING_FILM_SOUND = 24, _("テレビ・放送・映像・音響")
    DESIGN = 25, _("デザイン")
    MATERIAL = 26, _("素材")
    FOOD = 27, _("食品")
    COSMETICS = 28, _("化粧品")
    DAILY_GOODS = 29, _("日用品")
    REAL_ESTATE = 30, _("不動産")
    CONSTRUCTION_MANAGEMENT = 31, _("施工管理")
    MEDICAL_SALES = 32, _("医療営業")
    PRODUCTION_QUALITY_MANAGEMENT = 33, _("生産管理・品質管理・品質保証")
    ACADEMIC_PMS_REGULATORY = 34, _("学術・PMS・薬事")
    MEDICAL_NURSING_PHARMACY = 35, _("医療・看護・薬剤")
    UNKNOWN = 99, _("不明")


class Plan(models.IntegerChoices):
    """
    (選択肢) プラン
    """

    LITE = 1, _("Lite")
    BASIC = 2, _("Basic")
    PREMIUM = 3, _("Premium")


class Position(models.IntegerChoices):
    """
    (選択肢) 役職

    | 選択肢              | 選択肢(日本語)     | 値  |
    |---------------------|--------------------|-----|
    | PRESIDENT           | 経営者             | 1   |
    | SENIOR_ADVISER      | 役員               | 2   |
    | MANAGER             | 部長               | 3   |
    | SECTION_MANAGER     | 課長               | 4   |
    | UNIT_MANAGER        | 主任/係長          | 5   |
    | STAFF               | 一般社員           | 6   |
    """

    PRESIDENT = 1, _("経営者")
    SENIOR_ADVISER = 2, _("役員")
    MANAGER = 3, _("部長")
    SECTION_MANAGER = 4, _("課長")
    UNIT_MANAGER = 5, _("主任/係長")
    STAFF = 6, _("一般社員")


class Prefecture(models.IntegerChoices):
    """
    (選択肢) 都道府県

    | 選択肢      | 選択肢(日本語)      | 値  |
    |-------------|---------------------|-----|
    | HOKKAIDO    | 北海道              | 1   |
    | AOMORI      | 青森県              | 2   |
    | IWATE       | 岩手県              | 3   |
    | MIYAGI      | 宮城県              | 4   |
    | AKITA       | 秋田県              | 5   |
    | YAMAGATA    | 山形県              | 6   |
    | FUKUSHIMA   | 福島県              | 7   |
    | IBARAKI     | 茨城県              | 8   |
    | TOCHIGI     | 栃木県              | 9   |
    | GUNMA       | 群馬県              | 10  |
    | SAITAMA     | 埼玉県              | 11  |
    | CHIBA       | 千葉県              | 12  |
    | TOKYO       | 東京都              | 13  |
    | KANAGAWA    | 神奈川県            | 14  |
    | NIIGATA     | 新潟県              | 15  |
    | TOYAMA      | 富山県              | 16  |
    | ISHIKAWA    | 石川県              | 17  |
    | FUKUI       | 福井県              | 18  |
    | YAMANASHI   | 山梨県              | 19  |
    | NAGANO      | 長野県              | 20  |
    | GIFU        | 岐阜県              | 21  |
    | SHIZUOKA    | 静岡県              | 22  |
    | AICHI       | 愛知県              | 23  |
    | MIE         | 三重県              | 24  |
    | SHIGA       | 滋賀県              | 25  |
    | KYOTO       | 京都府              | 26  |
    | OSAKA       | 大阪府              | 27  |
    | HYOGO       | 兵庫県              | 28  |
    | NARA        | 奈良県              | 29  |
    | WAKAYAMA    | 和歌山県            | 30  |
    | TOTTORI     | 鳥取県              | 31  |
    | SHIMANE     | 島根県              | 32  |
    | OAKAYAMA    | 岡山県              | 33  |
    | HIROSHIMA   | 広島県              | 34  |
    | YAMAGUCHI   | 山口県              | 35  |
    | TOKUSHIMA   | 徳島県              | 36  |
    | KAGAWA      | 香川県              | 37  |
    | EHIME       | 愛媛県              | 38  |
    | KOCHI       | 高知県              | 39  |
    | FUKUOKA     | 福岡県              | 40  |
    | SAGA        | 佐賀県              | 41  |
    | NAGASAKI    | 長崎県              | 42  |
    | KUMAMOTO    | 熊本県              | 43  |
    | OITA        | 大分県              | 44  |
    | MIYAZAKI    | 宮崎県              | 45  |
    | KAGOSHIMA   | 鹿児島県            | 46  |
    | OKINAWA     | 沖縄県              | 47  |
    | OVERSEAS    | 海外                | 99  |
    """

    HOKKAIDO = 1, _("北海道")
    AOMORI = 2, _("青森県")
    IWATE = 3, _("岩手県")
    MIYAGI = 4, _("宮城県")
    AKITA = 5, _("秋田県")
    YAMAGATA = 6, _("山形県")
    FUKUSHIMA = 7, _("福島県")
    IBARAKI = 8, _("茨城県")
    TOCHIGI = 9, _("栃木県")
    GUNMA = 10, _("群馬県")
    SAITAMA = 11, _("埼玉県")
    CHIBA = 12, _("千葉県")
    TOKYO = 13, _("東京都")
    KANAGAWA = 14, _("神奈川県")
    NIIGATA = 15, _("新潟県")
    TOYAMA = 16, _("富山県")
    ISHIKAWA = 17, _("石川県")
    FUKUI = 18, _("福井県")
    YAMANASHI = 19, _("山梨県")
    NAGANO = 20, _("長野県")
    GIFU = 21, _("岐阜県")
    SHIZUOKA = 22, _("静岡県")
    AICHI = 23, _("愛知県")
    MIE = 24, _("三重県")
    SHIGA = 25, _("滋賀県")
    KYOTO = 26, _("京都府")
    OSAKA = 27, _("大阪府")
    HYOGO = 28, _("兵庫県")
    NARA = 29, _("奈良県")
    WAKAYAMA = 30, _("和歌山県")
    TOTTORI = 31, _("鳥取県")
    SHIMANE = 32, _("島根県")
    OKAYAMA = 33, _("岡山県")
    HIROSHIMA = 34, _("広島県")
    YAMAGUCHI = 35, _("山口県")
    TOKUSHIMA = 36, _("徳島県")
    KAGAWA = 37, _("香川県")
    EHIME = 38, _("愛媛県")
    KOCHI = 39, _("高知県")
    FUKUOKA = 40, _("福岡県")
    SAGA = 41, _("佐賀県")
    NAGASAKI = 42, _("長崎県")
    KUMAMOTO = 43, _("熊本県")
    OITA = 44, _("大分県")
    MIYAZAKI = 45, _("宮崎県")
    KAGOSHIMA = 46, _("鹿児島県")
    OKINAWA = 47, _("沖縄県")
    OVERSEAS = 99, _("海外")


class RangeType(models.IntegerChoices):
    """
    (選択肢) 範囲タイプ

    | 選択肢        | 選択肢(日本語)  | 値  |
    |---------------|----------------|-----|
    | MORE_TH       | 以上           | 1   |
    | LESS_THAN     | 未満           | 2   |
    """

    MORE_THAN = 1, _("以上")
    LESS_THAN = 2, _("未満")


class RelevanceLevel(models.IntegerChoices):
    """
    (選択肢) 関連度レベル

    | 選択肢             | 選択肢(日本語)       | 値  |
    |--------------------|----------------------|-----|
    | VERY_RELEVANT      | とても関連している   | 5   |
    | SOMEWHAT_RELEVANT  | やや関連している | 4   |
    | NEUTRAL_RELEVANCE  | どちらともいえない   | 3   |
    | SLIGHTLY_RELEVANT  | あまり関連していない | 2   |
    | NOT_RELEVANT       | 全く関連していない   | 1   |
    """

    VERY_RELEVANT = 5, _("とても関連している")
    SOMEWHAT_RELEVANT = 4, _("やや関連している")
    NEUTRAL_RELEVANCE = 3, _("どちらともいえない")
    SLIGHTLY_RELEVANT = 2, _("あまり関連していない")
    NOT_RELEVANT = 1, _("全く関連していない")


class RecruitmentMedia(models.IntegerChoices):
    """
    (選択肢) 求人媒体

    参考: https://www.neo-career.co.jp/humanresource/knowhow/a-contents-middlecareer-about_directrecruiting-200228/

    | 選択肢        | 選択肢(日本語)                | 値  |
    |---------------|-------------------------------|-----|
    | BIZREACH      | BIZREACH                      | 1   |
    | DODA          | dodaダイレクト                | 2   |
    | GREEN         | Green                         | 3   |
    | WANTEDLY      | Wantedly                      | 4   |
    | RICRUIT       | リクルート ダイレクトスカウト  | 5   |
    | MYNAVI        | マイナビ転職                  | 6   |
    | EN            | エン転職ダイレクト            | 7   |
    | AMBI          | AMBI                          | 8   |
    | LINKEDIN      | Linkedin                      | 9  |
    | PAIZA         | paiza                         | 10  |
    | OPEN_WORK     | OpenWork                      | 11  |
    | HRMOS     | HRMOS                         | 12  |
    | NISHIKA       | Nishika                       | 13  |
    | LEVTECH       | レバテックダイレクト          | 14  |
    | OWNED_MEDIA    | 自社メディア                   | 98  |
    | OTHER         | その他                        | 99  |
    """

    BIZREACH = 1, _("BIZREACH")
    DODA = 2, _("dodaダイレクト")
    GREEN = 3, _("Green")
    WANTEDLY = 4, _("Wantedly")
    RICRUIT = 5, _("リクルート ダイレクトスカウト")
    MYNAVI = 6, _("マイナビ転職")
    EN = 7, _("エン転職ダイレクト")
    AMBI = 8, _("AMBI")
    LINKEDIN = 9, _("Linkedin")
    PAIZA = 10, _("paiza")
    OPEN_WORK = 11, _("OpenWork")
    HRMOS = 12, _("HRMOS")
    NISHIKA = 13, _("Nishika")
    LEVTECH = 14, _("レバテックダイレクト")
    OWNED_MEDIA = 98, _("自社メディア")
    OTHER = 99, _("その他")


class RequirementCategory(models.IntegerChoices):
    """
    (選択肢) 求める人物像の要件のカテゴリ

    | 選択肢            | 選択肢    （日本語） | 値  |
    |-------------------|----------------------|-----|
    | SKILL             | スキル               | 1   |
    | EXPERIENCE        | 経験                 | 2   |
    | CERTIFICATION     | 資格                 | 3   |
    | LOCATION          | 希望勤務地           | 4   |
    | OTHER             | その他               | 99  |
    """ # noqa: RUF002

    SKILL = 1, _("スキル")
    EXPERIENCE = 2, _("経験")
    CERTIFICATION = 3, _("資格")
    LOCATION = 4, _("希望勤務地")
    OTHER = 99, _("その他")


class RequirementLevel(models.IntegerChoices):
    """
    (選択肢) 求める人物像の要求レベル

    | 選択肢            | 選択肢    （日本語） | 値  |
    |-------------------|----------------------|-----|
    | REQUIRED          | 必須                 | 1   |
    | OPTIONAL          | 任意                 | 2   |
    | REQUIRED_ONE_OF   | いずれか必須         | 3   |
    """ # noqa: RUF002

    REQUIRED = 1, _("必須")
    OPTIONAL = 2, _("任意")
    REQUIRED_ONE_OF = 3, _("いずれか必須")
