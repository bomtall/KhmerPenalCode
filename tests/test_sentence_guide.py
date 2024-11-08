import json
import pytest


from KhmerPenalCode.src.sentence_guide import SentenceGuide, Crime

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
    assert Crime(*args, **kwargs).crime == expected
    
test_sg_class = SentenceGuide(Crime(penal_dict['Theft']))

@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            (["Article 357"], dict(), 10),
            (["Article 358"], dict(), 20),
            (["Article 359"], dict(), 30),
            (["Article 360"], dict(), 30),
        ]
)
def test_set_agg_max(args, kwargs, expected):
    test_sg_class.set_agg_max_sentence(*args, **kwargs)
    assert test_sg_class.agg_max_sentence == expected
    
    
@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            (["Article 357"], dict(), 3),
            (["Article 358"], dict(), 10),
            (["Article 359"], dict(), 15),
            (["Article 360"], dict(), 15),
        ]
)
def test_set_agg_min(args, kwargs, expected):
    test_sg_class.set_agg_min_sentence(*args, **kwargs)
    assert test_sg_class.agg_min_sentence == expected
