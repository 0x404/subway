"""subway"""
import sys
from core import utils
from core.model import SubwaySys


def query_shortest_path(start, end):
    """Query shortest path.

    Args:
        start: start station name.
        end: end station name.

    Return:
        ansx: x position list.
        ansy: y position list.
    """
    lines = utils.load_lines("data/beijing-subway.txt")
    station_pos = utils.load_station_pos("data/beijing-subway-pos.txt")
    subway = SubwaySys(lines)
    path = subway.shortest_path(start, end)
    ansx, ansy = [], []
    for station, _ in path:
        ansx.append(station_pos[station.name][0])
        ansy.append(station_pos[station.name][1])
    return ansx, ansy


def query_travel_path(start):
    """Query travel path.

    Args:
        start: start station name.

    Return:
        ansx: x position list.
        ansy: y position list.
    """
    lines = utils.load_lines("data/beijing-subway.txt")
    station_pos = utils.load_station_pos("data/beijing-subway-pos.txt")
    subway = SubwaySys(lines)
    path = subway.travel_path_from(start)
    ansx, ansy = [], []
    for station in path:
        ansx.append(station_pos[station][0])
        ansy.append(station_pos[station][1])
    return ansx, ansy


def print_path(subway_sys, start, end):
    """
    print a path from start to end in subway_sys
    :param subway_sys: a subwaysys
    :param start: a string indicates start station's name
    :param end: a string indicates end station's name
    """
    path = subway_sys.shortest_path(start, end)
    print("总站数: ", len(path))
    for station, msg in path:
        print(station.name, msg if msg is not None else "")


def print_travel_path(subway_sys, start):
    """Print travel path.

    Print path that travel from start and pass all station.

    Args:
        subway_sys: subway system.
        start: str, start station.

    Return:
        None.
    """
    path = subway_sys.travel_path_from(start)
    print("总站数: ", len(path))
    for station in path:
        print(station)


def walk_side(subway_sys, file_path):
    """Test by file.

    Args:
        subway_sys: subway system.
        file_path: path of test file.

    Return:
        None.
    """
    path = utils.load_test_file(file_path)
    res = subway_sys.walk_side(path)
    print(res["stats"])
    if res["stats"] == "false":
        print("遗漏车站:", res["miss_st"])


def main():
    """
    subway system entry
    supported operation:
        subway.py /b <start_station_name> <end_station_name>
    """
    lines = utils.load_lines("data/beijing-subway.txt")
    subway = SubwaySys(lines)
    if len(sys.argv) == 4 and sys.argv[1] == "/b":
        print_path(subway, sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "/a":
        print_travel_path(subway, sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "/z":
        walk_side(subway, sys.argv[2])
    elif len(sys.argv) != 1:
        print("[error]: operation is supported!")
        print("[usage]: subway.py /b <start_station_name> <end_station_name>")
        return
    while True:
        command = input()
        if len(command) <= 0:
            continue
        command = utils.split_by_space(command)
        if command[0] == "/b" and len(command) == 3:
            print_path(subway, command[1], command[2])
        elif command[0] == "/a" and len(command) == 2:
            print_travel_path(subway, command[1])
        elif command[0] == "/z" and len(command) == 2:
            walk_side(subway, command[1])
        else:
            print("[error]: operation is not supported!")
            print("[usage]: subway.py /b <start_station_name> <end_station_name>")


if __name__ == "__main__":
    main()
