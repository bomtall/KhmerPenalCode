import KhmerPenalCode.src.utils as utils
import pytest

@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            ([1], dict(), 365),
            ([0.5], dict(), 183),
            ([6/365], dict(), 6)
            
        ]
)
def test_convert_years_to_days(args, kwargs, expected):
    assert utils.convert_years_to_days(*args, **kwargs) == expected
    
@pytest.mark.parametrize(
        'args,kwargs,expected', 
        [
            ([6], dict(), 0.02),
            ([365], dict(), 1),
            ([182], dict(), 0.5),
            ([183], dict(), 0.5)           
        ]
)
def test_days_to_years(args, kwargs, expected):
    assert utils.convert_days_to_years(*args, **kwargs) == expected