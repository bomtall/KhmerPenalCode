import json
import pytest
import conftests
from KhmerPenalCode.src import utils

# execute from folder above
# python -m pip install c:/Users/bc975546/code/KhmerPenalCode
# command to run: pytest tests

# with open("../resources/data.json", "r") as f:
#     penal_dict = json.load(f)

@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            ([], {"Theft": {"crime": "Theft"}}, ["Theft"]),
        ]
)
def test_sentence_guide(args, kwargs, expected):
    assert utils.SentenceGuide(*args, **kwargs).crime == expected
