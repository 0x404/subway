import sys


def generate_data(data_path, target_path):
    """
    :param data_path: 源数据路径
    :param target_path: 生成数据路径
        源数据文件格式：

            #路线名1    (#表示接下来为一条地铁线)
            站点名1 站点名2 ... 站点名n
            #$路线名2   ($表示该路线为环形)
            站点名1 站点名2 ... 站点名n
            ...
            #           (文件最后一定以#结尾)

        生成数据文件格式：

            L 路线名1 1/0    # L 表示地铁线，1/0表示该地铁线是否为环形
            站点名1 1/0      # 1/0表示该站点是否为换乘站
            站点名2 1/0
            ...
            站点名n 1/0
            L 路线名2 1/0
            站点名1 1/0
            站点名2 1/0
            ...
            站点名n 1/0
            ...
    """
    ring = False
    line_name = ""
    data, st_list = [], []

    file = open(data_path, mode="r", encoding="utf-8")
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        line = line.split(" ")
        for station in line:
            if station[0] == "#":
                if len(st_list) > 0:
                    data.append(
                        {"line": line_name, "ring": ring, "station_list": st_list}
                    )
                    ring = False
                    line_name = ""
                    st_list = []
                station = station[1:]
                if len(station) > 0 and station[0] == "$":
                    ring = True
                    station = station[1:]
                line_name = station
            else:
                st_list.append({"station_name": station, "transfer": False})
    file.close()
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            for st_i in data[i]["station_list"]:
                for st_j in data[j]["station_list"]:
                    if st_i["station_name"] == st_j["station_name"]:
                        st_i["transfer"] = st_j["transfer"] = True

    file = open(target_path, mode="w", encoding="utf-8")
    for line in data:
        file.write("L " + line["line"] + " " + ("1" if line["ring"] else "0") + "\n")
        for station in line["station_list"]:
            file.write(
                station["station_name"]
                + " "
                + ("1" if station["transfer"] else "0")
                + "\n"
            )
    file.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("parameter error!")
        print("python build.py source_path target_path")
        print(
            "example : python build.py data/beijing-subway-raw.txt data/beijing-subway.txt"
        )
    else:
        generate_data(sys.argv[1], sys.argv[2])
        print("finished!")
