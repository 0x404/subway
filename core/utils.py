"""utils"""
# pylint: disable=simplifiable-if-expression
from core.model import Station
from core.model import Line


def load_lines(data_path):
    """Load subway lines from data file.

    Args:
        data_path: the path of subway data, specificaly `data/beijing-subway.txt`

    Return:
        list: a list of Line object, e.g. [Line1, Line2, ...]
    """

    line_name = ""
    station_list, lines = [], []
    is_ring = False

    file = open(data_path, mode="r", encoding="utf-8")
    while True:
        strs = file.readline()
        if not strs and len(station_list) > 0:
            lines.append(
                Line(line_name=line_name, st_list=station_list, is_ring=is_ring)
            )
            break
        strs = strs.strip("\n").strip()
        strs = strs.split(" ")
        if strs[0] == "L":
            if len(station_list) > 0:
                lines.append(
                    Line(line_name=line_name, st_list=station_list, is_ring=is_ring)
                )
            line_name = strs[1]
            station_list = []
            is_ring = True if strs[2] == "1" else False
        else:
            station_list.append(Station(strs[0], True if strs[1] == "1" else False))
    file.close()
    return lines


def load_test_file(data_path):
    """Load test file.

    Args:
        data_path: the path of test data

    Return:
        list: list of station name, e.g. ["海淀黄庄", "知春路", "知春里", ...]
    """
    lines = []
    with open(data_path, encoding="utf-8") as file:
        for _, line in enumerate(file):
            line = line.strip("\n").strip()
            line = split_by_space(line)
            lines += line
    return lines


def split_by_space(inputs):
    """Split str by space.

    Args:
        inputs: str, e.g. "x  y z  ww e  "

    Return:
        list of strs, e.g. ["x", "y", "z", "ww", "e"]
    """
    ans = []
    now_str = ""
    length = len(inputs)
    for index in range(length):
        if inputs[index] == " ":
            if len(now_str) > 0:
                ans.append(now_str)
                now_str = ""
        else:
            now_str = now_str + inputs[index]
    if len(now_str) > 0:
        ans.append(now_str)
    return ans
