import pytest

from smirnybot9001.util import is_identifier, parse_bricklink_meta_description


@pytest.mark.parametrize("test_input", (112, '123', 'col-34', 786454, 'huhuhu'))
def test_valid_set_number(test_input):
    assert is_identifier(test_input)


@pytest.mark.parametrize("test_input", ("WUT" * 128, 'ÄÖÜ', '////', '(-', '300?',))
def test_invalid_set_number(test_input):
    assert not is_identifier(test_input)


def test_parse_bricklink_meta_description():
    md = "ItemName: LEGO Spider Lady, Series 14 (Complete Set with Stand and Accessories), ItemType: Set, ItemNo: col14-16, Buy and sell LEGO parts, Minifigures and sets, both new or used from the world's largest online LEGO marketplace."
    thing_name, thing_type, thing_nr = parse_bricklink_meta_description(md)
    assert thing_name == 'Spider Lady, Series 14 (Complete Set with Stand and Accessories)'
    assert thing_type == 'Set'
    assert thing_nr == 'col14-16'
