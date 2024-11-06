from base.tests.factories.company import CompanyFactory
from base.tests.factories.work_value import WorkValueFactory


def run():
    work_values = WorkValueFactory()
    print(f'Created work value: {work_values.work_value}')

    company = CompanyFactory(name='株式会社テスト')
    print(f'Created company: {company.name}')





