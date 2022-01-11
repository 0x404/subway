import utils
from model import SubwaySys


if __name__ == "__main__":
    lines = utils.load_lines("../data/beijing-subway.txt")
    subway = SubwaySys(lines)
    # subway.test_by_file("../data/testfile.txt")

    while True:
        cmd = input()
        cmd = cmd.strip().split(" ")
        if cmd[0] == "a" and len(cmd) == 3:
            path = subway.shortest_path(cmd[1], cmd[2])
            print(len(path))
            for station in path:
                if station.is_trans:
                    print(station.name, " 换乘")
                else:
                    print(station.name)
