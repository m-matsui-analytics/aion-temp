import datetime

import pytest

from base.models.company import Company
from base.models.company_info import CompanyInfo


# @pytest.mark.django_db(databases=["default"])
# @pytest.mark.django_db
# @pytest.fixture(scope="session")
# @pytest.fixture
def set_base_company_info(company: Company) -> None:
    """Set company_info data."""
    CompanyInfo.objects.filter(company=company).update(
        company=company,
        foundation_date=datetime.date(2021, 8, 15),
        capital=1000,
        address_prefecture=14,
        address_other="藤沢市藤沢484-1 藤沢アンバービル4階",
        ceo_name="溝口 大作",
        employee_size=3,
        business_description="データ分析・システムインテグレーション",
        industry=1,
        revenue=1000,
        mission="私たちはデータ分析を目的とするのではなくその先にある「顧客の課題解決」を目的としています。データ分析は、あくまで課題解決の手段にすぎません。ただ、データ分析はこれまでの常識を打破しより速く、より正確な意思決定を可能にする手段であるため現代においては、どの業界でも必要不可欠なものとなっています。その分野で我々は、日々お客様に向き合い世の中のあらゆる課題解決を支援しております。",
        vision="日本には、世界に誇るべき技術や文化が多くある一方、少子高齢化や経済活動の衰退などの課題が山積みです。分析という手段を用いて、こういった課題を一つずつ解決していくことでより良い社会を実現することができると信じています。分析屋では、様々なバックグラウンドを持つ方がそれぞれの場所で働いていますが皆、「よりよい社会にしたい」という思いは一緒です",
        value="ただ依頼された業務をその通りにこなし分析結果をそのままお渡しすることは、ただの集計作業にすぎません。私たちが提供するのは分析結果に「おもてなし」を添えてお伝えする課題解決支援サービスです。例えば、難しい分析手法を用いたとしてもお客様に分析結果を活用していただけなければ、意味がありません。分析屋では、分析結果にどのような意味があるのかそこからどういった判断ができそうなのかを併せてお伝えするまでがデータ分析支援のあるべき形と考えております。"
    )
