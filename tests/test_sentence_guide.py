import json
import pytest

# go to pyproject.toml and set property pythonpath as path to project

from KhmerPenalCode.src.sentence_guide import SentenceGuide

# command to run: pytest tests

with open("resources/data.json", "r") as f:
    penal_dict = json.load(f)

@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            ([penal_dict["Theft"]], dict(), "Theft"),
            ([penal_dict["Murder"]], dict(), "Murder"),
        ]
)
def test_sentence_guide(args, kwargs, expected):
    assert SentenceGuide(*args, **kwargs).crime == expected
    

@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            (["Article 357"], dict(), 10),
            (["Article 358"], dict(), 20),
            (["Article 359"], dict(), 30),
        ]
)
def test_set_agg_max(args, kwargs, expected):
    obj = SentenceGuide(penal_dict["Theft"])
    obj.set_agg_max_sentence(*args, **kwargs)
    assert obj.agg_max_sentence == expected
    
    
@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            (["Article 357"], dict(), 3),
            (["Article 358"], dict(), 10),
            (["Article 359"], dict(), 15),
        ]
)
def test_set_agg_min(args, kwargs, expected):
    obj = SentenceGuide(penal_dict["Theft"])
    obj.set_agg_min_sentence(*args, **kwargs)
    assert obj.agg_min_sentence == expected
