import pytest

from smirnybot9001.config import MAX_DURATION
from smirnybot9001.chatbot import parse_set_command, BadCommandValue

VALID_SET_INPUTS = (({1: '1'}, '1', 23),
                    ({1: 'as'}, 'as', 23),
                    ({1: 'as', 2: 33}, 'as', 33),
                    ({1: 'as', 2: '33'}, 'as', 33),
                    ({1: 'as', 2: '33'}, 'as', 33),
({1: 'as', 2: MAX_DURATION + 10}, 'as', MAX_DURATION),

                    )
INVALID_SET_INPUTS = ({},
                      {1: 'öüä'},
                      {1: ''},
                      {1: 'öüä', 2: 'öpo'},
                      {1: '123', 2: ''},
                      {1: '', 2: ''},
                      )


@pytest.mark.parametrize('words', INVALID_SET_INPUTS)
def test_invalid_set_commands(words):
    with pytest.raises(BadCommandValue):
        parse_set_command(words, 23)


@pytest.mark.parametrize('words, expected_nr, expected_duration', VALID_SET_INPUTS)
def test_valid_set_commands(words, expected_nr, expected_duration):
    nr, duration = parse_set_command(words, 23)
    assert nr == expected_nr
    assert duration == expected_duration

