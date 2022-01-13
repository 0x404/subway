"""subway"""
import sys
from core import utils
from core.model import SubwaySys


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
    elif len(sys.argv) != 1:
        print("[error]: operation is supported!")
        print("[usage]: subway.py /b <start_station_name> <end_station_name>")
        return
    while True:
        command = input()
        command = command.strip().split(" ")
        if command[0] == "/b" and len(command) == 3:
            print_path(subway, command[1], command[2])
        else:
            print("[error]: operation is supported!")
            print("[usage]: subway.py /b <start_station_name> <end_station_name>")


if __name__ == "__main__":
    main()
