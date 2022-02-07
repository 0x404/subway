"""pytest for core/model.py"""

from core.model import *
from core import utils


def test_add_line():
    test1_line1 = Line(
        "A",
        [Station("a_1"), Station("a_2"), Station("a_3"), Station("a_4")],
        is_ring=True,
    )
    test1_line2 = Line("B", [Station("b_1"), Station("a_1"), Station("b_2")])
    test1_line3 = Line("C", [Station("a_2"), Station("b_1"), Station("c_1")])
    subway = SubwaySys([test1_line1, test1_line2, test1_line3])
    assert len(subway.nexto) == 7 and len(subway.lines) == 3
    assert sorted([edge.station_to for edge in subway.nexto["a_1"]]) == [
        "a_2",
        "a_4",
        "b_1",
        "b_2",
    ]
    assert sorted([edge.station_to for edge in subway.nexto["a_2"]]) == [
        "a_1",
        "a_3",
        "b_1",
    ]
    assert sorted([edge.station_to for edge in subway.nexto["b_1"]]) == [
        "a_1",
        "a_2",
        "c_1",
    ]
    assert sorted([edge.station_to for edge in subway.nexto["a_3"]]) == ["a_2", "a_4"]
    assert sorted([edge.station_to for edge in subway.nexto["a_4"]]) == ["a_1", "a_3"]
    assert sorted([edge.station_to for edge in subway.nexto["b_2"]]) == ["a_1"]
    assert sorted([edge.station_to for edge in subway.nexto["c_1"]]) == ["b_1"]


def test_shortest_path():
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)
    test_input1 = ["知春路", "中关村"]
    test_output1 = subway.shortest_path(test_input1[0], test_input1[1])
    test_output1 = [st.name for st, _ in test_output1]
    test_ans1 = ["知春路", "知春里", "海淀黄庄", "中关村"]
    assert test_output1 == test_ans1

    test_input2 = ["宣武门", "复兴门"]
    test_output2 = subway.shortest_path(test_input2[0], test_input2[1])
    test_output2 = [st.name for st, _ in test_output2]
    test_ans2_1 = ["宣武门", "西单", "复兴门"]
    test_ans2_2 = ["宣武门", "长椿街", "复兴门"]
    assert test_output2 == test_ans2_1 or test_output2 == test_ans2_2

    test_input3 = ["北京西站", "西局"]
    test_output3 = subway.shortest_path(test_input3[0], test_input3[1])
    test_output3 = [st.name for st, _ in test_output3]
    test_ans3 = ["北京西站", "六里桥东", "六里桥", "西局"]
    assert test_output3 == test_ans3


def test_travel_path_from():
    test1_line1 = Line(
        "A",
        [Station("a_1"), Station("a_2"), Station("a_3"), Station("a_4")],
        is_ring=True,
    )
    test1_line2 = Line("B", [Station("b_1"), Station("a_1"), Station("b_2")])
    test1_line3 = Line("C", [Station("a_2"), Station("b_1"), Station("c_1")])
    subway = SubwaySys([test1_line1, test1_line2, test1_line3])

    test1_pred1 = subway.travel_path_from("a_1")
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

    test1_pred2 = subway.travel_path_from("b_1")
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

    test1_pred3 = subway.travel_path_from("a_2")
    test1_ans3 = ["a_2", "b_1", "c_1", "b_1", "a_1", "b_2", "a_1", "a_2", "a_3", "a_4"]
    assert test1_pred3 == test1_ans3
