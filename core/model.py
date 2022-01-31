"""model"""
INF: int = 10000
from core import solution


class Station:
    """
    station class
    """

    def __init__(self, st_name, is_trans=False):
        self.station_name = st_name
        self.trans = is_trans

    @property
    def name(self):
        """get station's name"""
        return self.station_name

    @property
    def is_trans(self):
        """whther a station is a transfer station"""
        return self.trans

    def __str__(self):
        if self.trans:
            return "station(%s, transfer_st)" % (self.station_name)
        return "station(%s, normal_st)" % (self.station_name)


class Edge:
    """
    line edge
    :param st_j(str)        : Edge visited station
    :param line_belongs(str): this edge belongs which line
    """

    def __init__(self, station_to, belong_to):
        self.st_j = station_to
        self.line_belongs = belong_to

    @property
    def station_to(self):
        """which station an edge link to"""
        return self.st_j

    @property
    def belong_to(self):
        """which line an edge belong to"""
        return self.line_belongs


class Line:
    """
    line class, consists of stations
    """

    def __init__(self, line_name, st_list, is_ring=False):
        self.line_name = line_name
        self.st_list = st_list
        self.ring = is_ring
        self.start = st_list[0].name
        self.end = st_list[-1].name
        self.length = len(st_list)

    @property
    def name(self):
        """a line's name"""
        return self.line_name

    @property
    def is_ring(self):
        """whether the line is a ring"""
        return self.ring

    @property
    def station_list(self):
        """get station list of a line"""
        return self.st_list

    def __str__(self):
        return "地铁线: " + self.line_name


class SubwaySys:
    """
    subwaySys class, consists of lines
    """

    def __init__(self, line_list=None):
        self.str2st = {}  # station_name -> station
        self.nexto = {}  # station_name -> edge
        self.lines = []
        if line_list is not None:
            for line in line_list:
                self.add_line(line)

    def get_edge_belongs(self, st_i, st_j):
        """
        :param st_i: station name one
        :param st_j: station name two
        :return: line_name
        """
        if isinstance(st_i, Station):
            st_i = st_i.name
        if isinstance(st_j, Station):
            st_j = st_j.name

        for nxt_ed in self.nexto[st_i]:
            if nxt_ed.station_to == st_j:
                return nxt_ed.belong_to
        raise Exception(
            "[error]: get_edge_belongs--" + st_i + " " + st_j + " not connected."
        )

    def is_next(self, st_i, st_j):
        """
        :param   st_i: origin station (str)
        :param   st_j: judged station (str)
        :return: st_j whether next to st_i
        """
        for nex_ed in self.nexto[st_i]:
            if nex_ed.station_to == st_j:
                return True
        return False

    def add_line(self, line):
        """
        add line to subway system
        :param line: a line object
        """
        self.lines.append(line)
        for i in range(len(line.station_list) - 1):
            self._link(line.station_list[i], line.station_list[i + 1], line.name)
        if line.is_ring and len(line.station_list) > 1:
            self._link(line.station_list[0], line.station_list[-1], line.name)

    def _decorate_path(self, path):
        """
        decorate station list generate from algs (e.g. shortest_path)
        :param path: list of stations, e.g. [station1, station2, ..., station n]
        :return : list of [station, msg], e.g. [[station1, msg1], [station2, msg2], ...]
        """
        assert len(path) >= 1, "path to be decorated is empty."

        ans = [[path[0], None]]
        if len(path) == 1:
            return ans

        now_line = self.get_edge_belongs(path[0], path[1])
        for i in range(1, len(path) - 1):
            nex_line = self.get_edge_belongs(path[i], path[i + 1])
            if now_line != nex_line:
                ans.append([path[i], "换乘" + nex_line])
                now_line = nex_line
            else:
                ans.append([path[i], None])
        ans.append([path[-1], None])
        return ans

    def shortest_path(self, start, end):
        """
        calculate the shortest path from star station to end station
        :param start: start station object or the name of start station
        :param end: end station object or the name of end station
        :return : a list of station object presents the path from start to the end
        """
        if isinstance(start, str):
            assert start in self.str2st, "station {} is not in subway system.".format(
                start
            )
        else:
            start = start.name
        if isinstance(end, str):
            assert end in self.str2st, "station {} is not in subway system.".format(end)
        else:
            end = end.name

        ans_path = solution.shortest_path(start, end, self.nexto)
        ans_path = list(map(lambda x: self.str2st[x], ans_path))
        return self._decorate_path(ans_path)

    def travel_path_from(self, start):
        """Calculate the travel path.

        Calculate the path that travels all station.

        Args:
            start: str or station object, indicats the start station.

        Return:
            A list of station name indicates the path.
        """
        if isinstance(start, str):
            assert start in self.str2st, "station {} is not in subway system".format(
                start
            )
        else:
            start = start.name
        return solution.travel_path_from(start, self.nexto, self.lines)

    def _link(self, st_i, st_j, edge_belong):
        """
        create an edge between station i and station j
        :param st_i: a station object
        :param st_j: a station object
        """
        if st_i.name not in self.str2st:
            self.str2st[st_i.name] = Station(st_i.name, st_i.is_trans)
        if st_j.name not in self.str2st:
            self.str2st[st_j.name] = Station(st_j.name, st_j.is_trans)

        st_i = self.str2st[st_i.name]
        st_j = self.str2st[st_j.name]

        if st_i.name not in self.nexto:
            self.nexto[st_i.name] = []
        if st_j.name not in self.nexto:
            self.nexto[st_j.name] = []

        if not self.is_next(st_i=st_j.name, st_j=st_i.name):
            self.nexto[st_j.name].append(
                Edge(station_to=st_i.name, belong_to=edge_belong)
            )
        if not self.is_next(st_i=st_i.name, st_j=st_j.name):
            self.nexto[st_i.name].append(
                Edge(station_to=st_j.name, belong_to=edge_belong)
            )

    def test_by_file(self, file_path):
        """
        test all subways by file of path
        :param file_path: path of test file
        """
        visited = []
        file = open(file_path, mode="r", encoding="utf-8")

        while True:
            test_line = file.readline()
            if not test_line:
                break
            test_line = test_line.strip("\n").strip()
            test_line = test_line.split(" ")

            # 当前线路是否连接合法
            for index in range(len(test_line) - 1):
                if test_line[index] not in self.str2st:
                    print("error")
                    return
                if test_line[index + 1] not in self.str2st:
                    print("error")
                    return

                # 已访问的站点
                if test_line[index] not in visited:
                    visited.append(test_line[index])
                if test_line[index + 1] not in visited:
                    visited.append(test_line[index + 1])

                if not self.is_next(st_i=test_line[index], st_j=test_line[index + 1]):
                    print(
                        "error! 不合理的站点连接: "
                        + test_line[index]
                        + " "
                        + test_line[index + 1]
                    )
                    return

        for name in self.str2st:
            if str(name) not in visited:
                print("false! 未访问的站点: " + str(name))
