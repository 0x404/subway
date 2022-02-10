"""pytest for solution"""
from tkinter import N
from core.model import *
from core import utils
from core import solution


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
    tmp_output1 = solution.docorate_path(test_input1, subway.nexto)
    test_output1 = []
    for st in tmp_output1:
        test_output1.append([st[0].name, st[1]])

    assert test_output1 == test_ans1

    test_input2 = [Station("宣武门", True), Station("西单", True), Station("复兴门", True)]
    test_ans2 = [["宣武门", None], ["西单", "换乘1号线"], ["复兴门", None]]
    tmp_output2 = solution.docorate_path(test_input2, subway.nexto)
    test_output2 = []
    for st in tmp_output2:
        test_output2.append([st[0].name, st[1]])

    assert test_output2 == test_ans2


def test_get_edge_belongs():
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)

    assert solution.get_line_belong("宣武门", "西单", subway.nexto) == "4号线"
    assert solution.get_line_belong("白石桥南", "国家图书馆", subway.nexto) == "9号线"
    assert solution.get_line_belong("和平西桥", "和平里北街", subway.nexto) == "5号线"
    assert solution.get_line_belong("郭公庄", "大葆台", subway.nexto) == "房山线"


def test_is_next():
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)

    assert solution.is_nexto("郭公庄", "稻田", subway.nexto) == False
    assert solution.is_nexto("北海北", "什刹海", subway.nexto) == False
    assert solution.is_nexto("东单", "王府井", subway.nexto) == True
    assert solution.is_nexto("七里庄", "西局", subway.nexto) == True
    assert solution.is_nexto("七里庄", "六里桥", subway.nexto) == True
    assert solution.is_nexto("七里庄", "泥洼", subway.nexto) == False


def test_travel_path_from():
    test1_line1 = Line(
        "A",
        [Station("a_1"), Station("a_2"), Station("a_3"), Station("a_4")],
        is_ring=True,
    )
    test1_line2 = Line("B", [Station("b_1"), Station("a_1"), Station("b_2")])
    test1_line3 = Line("C", [Station("a_2"), Station("b_1"), Station("c_1")])
    test1_data = SubwaySys([test1_line1, test1_line2, test1_line3])

    test1_pred1 = solution.travel_path_from("a_1", test1_data.nexto, test1_data.lines)
    test1_ans1 = [
        "a_1",
        "a_2",
        "a_3",
        "a_4",
        "a_1",
        "b_1",
        "a_1",
        "b_2",
        "a_1",
        "a_2",
        "b_1",
        "c_1",
    ]
    assert test1_pred1 == test1_ans1

    test1_pred2 = solution.travel_path_from("b_1", test1_data.nexto, test1_data.lines)
    test1_ans2 = [
        "b_1",
        "a_1",
        "b_2",
        "a_1",
        "a_2",
        "a_3",
        "a_4",
        "a_3",
        "a_2",
        "b_1",
        "c_1",
    ]
    assert test1_pred2 == test1_ans2

    test1_pred3 = solution.travel_path_from("a_2", test1_data.nexto, test1_data.lines)
    test1_ans3 = ["a_2", "b_1", "c_1", "b_1", "a_1", "b_2", "a_1", "a_2", "a_3", "a_4"]
    assert test1_pred3 == test1_ans3


def test_verify_path():
    test1_line1 = Line(
        "A",
        [Station("a_1"), Station("a_2"), Station("a_3"), Station("a_4")],
        is_ring=True,
    )
    test1_line2 = Line("B", [Station("b_1"), Station("a_1"), Station("b_2")])
    test1_line3 = Line("C", [Station("a_2"), Station("b_1"), Station("c_1")])
    test1_data = SubwaySys([test1_line1, test1_line2, test1_line3])

    test1_input1 = ["a_1", "a_2", "a_3", "a_4", "b_1", "b_2", "c_1"]
    test1_pred1 = solution.verify_path(test1_input1, test1_data.nexto)
    assert test1_pred1["stats"] == "error"

    test1_input2 = ["a_1", "a_2", "a_3", "a_4", "a_1", "b_1", "c_1"]
    test1_pred2 = solution.verify_path(test1_input2, test1_data.nexto)
    assert test1_pred2["stats"] == "false" and test1_pred2["miss_st"] == ["b_2"]

    test1_input3 = ["b_2", "a_1", "b_1", "c_1", "b_1", "a_1", "a_4", "a_3", "a_2"]
    test1_pred3 = solution.verify_path(test1_input3, test1_data.nexto)
    assert test1_pred3["stats"] == "true"
