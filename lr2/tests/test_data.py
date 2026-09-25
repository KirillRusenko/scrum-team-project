from jelinski_moranda.data import INTERVALS


def test_intervals():
    assert len(INTERVALS) == 26
    assert sum(INTERVALS) == 250
