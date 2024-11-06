from pathlib import Path

from base.models.company import Company
from base.models.company_strength import CompanyStrength


def set_base_company_strengths(company: Company) -> None:
    """Set company_strength data."""
    with Path.open(
            "src/base/tests/fixtures/data/company_strengths.txt",
            encoding="utf-8"
        ) as f:
        file_content = f.read()
        strength_list = file_content.split("\n")

    for strength in strength_list:
        CompanyStrength.objects.create(
            company=company,
            strength=strength
        )
