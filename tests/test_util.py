import pytest

from smirnybot9001.util import is_identifier


@pytest.mark.parametrize("test_input", (112, '123', 'col-34', 786454, 'huhuhu'))
def test_valid_set_number(test_input):
    assert is_identifier(test_input)


@pytest.mark.parametrize("test_input", ("WUT"*128, 'ÄÖÜ', '////', '(-', '300?', ))
def test_invalid_set_number(test_input):
    assert not is_identifier(test_input)
