"""pytest for core/model.py"""

from core.model import *
from core import utils


def test_decorate_path():
    lines = utils.load_lines("data/beijing-subway.txt")
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

    test_input2 = [
        Station("宣武门", True),
        Station("西单", True),
        Station("复兴门", True)
    ]
    test_ans2 = [["宣武门", None], ["西单", "换乘1号线"], ["复兴门", None]]
    tmp_output2 = subway._decorate_path(test_input2)
    test_output2 = []
    for st in tmp_output2:
        test_output2.append([st[0].name, st[1]])
    
    assert test_output2 == test_ans2

def test_get_edge_belongs():
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)
    
    assert subway.get_edge_belongs("宣武门", "西单") == "4号线"
    assert subway.get_edge_belongs("白石桥南", "国家图书馆") == "9号线"
    assert subway.get_edge_belongs("和平西桥", "和平里北街") == "5号线"
    assert subway.get_edge_belongs("郭公庄", "大葆台") == "房山线"

def test_is_next():
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)

    assert subway.is_next("郭公庄", "稻田") == False
    assert subway.is_next("北海北", "什刹海") == False
    assert subway.is_next("东单", "王府井") == True
    assert subway.is_next("七里庄", "西局") == True
    assert subway.is_next("七里庄", "六里桥") == True
    assert subway.is_next("七里庄", "泥洼") == False