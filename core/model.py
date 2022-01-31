"""model"""
from core import solution


class Station:
    """
    station class
    """

    def __init__(self, st_name, is_trans=False):
        self._name = st_name
        self._trans = is_trans

    @property
    def name(self):
        """get station's name"""
        return self._name

    @property
    def is_trans(self):
        """whther a station is a transfer station"""
        return self._trans

    def __str__(self):
        if self._trans:
            return "station(%s, transfer_st)" % (self._name)
        return "station(%s, normal_st)" % (self._name)


class Edge:
    """
    line edge
    """

    def __init__(self, station_to, belong_to):
        self._station_to = station_to
        self._belong_to = belong_to

    @property
    def station_to(self):
        """which station an edge link to"""
        return self._station_to

    @property
    def belong_to(self):
        """which line an edge belong to"""
        return self._belong_to


class Line:
    """
    line class, consists of stations
    """

    def __init__(self, line_name, st_list, is_ring=False):
        self._name = line_name
        self._st_list = st_list
        self._ring = is_ring

    @property
    def name(self):
        """a line's name"""
        return self._name

    @property
    def is_ring(self):
        """whether the line is a ring"""
        return self._ring

    @property
    def station_list(self):
        """get station list of a line"""
        return self._st_list

    @property
    def start(self):
        """name of the first station"""
        assert len(self._st_list) > 0
        return self._st_list[0].name

    @property
    def end(self):
        """name of the last station"""
        assert len(self._st_list) > 0
        return self._st_list[-1].name

    @property
    def length(self):
        """length of line"""
        return len(self._st_list)

    def __str__(self):
        return "地铁线: " + self._name


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
        """Get edge belong.

        Get the name of line that connect station i and station j.

        Args:
            st_i: str or station instance
            st_j: str or station instance

        Return:
            the line name of edge(station i, station j)
        """
        if isinstance(st_i, Station):
            st_i = st_i.name
        if isinstance(st_j, Station):
            st_j = st_j.name
        for nxt_ed in self.nexto[st_i]:
            if nxt_ed.station_to == st_j:
                return nxt_ed.belong_to

        raise Exception(
            "[error]: get_edge_belongs " + st_i + " " + st_j + " not connected."
        )

    def is_next(self, st_i, st_j):
        """Whether station i is next to station j.

        Args:
            st_i: str, name of station.
            st_j: str, name of station.

        Return:
            bool, true if station i is next to station j.
        """
        for nex_ed in self.nexto[st_i]:
            if nex_ed.station_to == st_j:
                return True
        return False

    def add_line(self, line):
        """Add a line to subway system.

        Args:
            line: line object to be added.
        """
        self.lines.append(line)
        for i in range(len(line.station_list) - 1):
            self._link(line.station_list[i], line.station_list[i + 1], line.name)
        if line.is_ring and len(line.station_list) > 1:
            self._link(line.station_list[0], line.station_list[-1], line.name)

    def shortest_path(self, start, end):
        """Calculate shortest path form start to end.

        Args:
            start: str or station obejct, indicates start station
            end: str or station object, indicates end station

        Return:
            a decorated shortest path,
            e.g.[[start, msg], [station, msg1], ..., [end, msg]]
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
        """Link station i and station j in subway system.

        Args:
            st_i: station object
            st_j: station object

        Return:
            None
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

    def _decorate_path(self, path):
        """Decorate path.

        Decorate station name list into station with message.

        Args:
            path: station list, e.g. [station1, station2, station3]

        Return:
            list: [[station1, msg1], [station2, msg2], [station3, msg3]].
            station: station instance.
            msg: str or None.
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
