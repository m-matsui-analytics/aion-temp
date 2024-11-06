import pytest
from django.core.management import call_command


@pytest.fixture(autouse=True)
def reset_db() -> None:
    """Reset the database before each test."""
    call_command('flush', '--noinput')
