from model import Station
from model import Line


def load_lines(data_path):
    """
    from data file read liens
    :param data_path: the path of data, specificaly data/beijing-subway.txt
    :return : a list of line, [line1, line2, ..., linen]
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
            lines.append(
                Line(line_name=line_name, st_list=station_list, is_ring=is_ring)
            )
            line_name = strs[1]
            station_list = []
            is_ring = True if strs[2] == "1" else False
        else:
            station_list.append(Station(strs[0], True if strs[1] == "1" else False))
    return lines
