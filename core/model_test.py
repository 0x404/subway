"""pytest for core/model.py"""

from model import *
import utils


def test_decorate_path():
    lines = utils.load_lines("../data/beijing-subway.txt")
    subway = SubwaySys(lines)
    test_input1 = [
        Station("大葆台", False),
        Station("郭公庄", True),
        Station("丰台科技园", False),
        Station("科怡路", False),
    ]
    test_ans1 = [["大葆台", None], ["郭公庄", "换乘9号线"], ["丰台科技园", None], ["科怡路", None]]
    tmp_output1 = subway._decorate_path(test_input1)
    test_output1 = []
    for st in tmp_output1:
        test_output1.append([st[0].name, st[1]])

    assert test_output1 == test_ans1
