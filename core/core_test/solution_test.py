"""pytest for solution"""
from core.model import *
from core import solution


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
