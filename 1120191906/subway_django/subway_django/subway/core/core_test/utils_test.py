"""pytest for core/utils.py"""
from core import utils


def test_split_by_space():
    assert utils.split_by_space("x w nsjd1 1 ") == ["x", "w", "nsjd1", "1"]
    assert utils.split_by_space(" qwe  ") == ["qwe"]
    assert utils.split_by_space("      ") == []
    assert utils.split_by_space(" 12    2  2 2 2") == ["12", "2", "2", "2", "2"]


def test_load_test_file():
    assert utils.load_test_file("data/testfile.txt") == [
        "良乡大学城",
        "良乡大学城北",
        "中关村",
        "知春路",
        "知春里",
    ]
