"""model"""
INF: int = 10000


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
        self.str2st = {}    # station_name -> station
        self.nexto = {}     # station_name -> edge
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

        for nxt_ed in self.nexto[st_i.name]:
            if nxt_ed.station_to == st_j:
                return nxt_ed.belong_to
        raise Exception(
            "SubwaySys_get_edge_belongs: " + st_i + " " + st_j + " not connected."
        )

    def is_next(self, st_i_name, st_j_name):
        """
        :param   st_i_name: origin station (str)
        :param   st_j_name: judged station (str)
        :return: st_j whether next to st_i
        """
        for nex_ed in self.nexto[st_i_name]:
            if nex_ed.station_to == st_j_name:
                return True
        return False

    def add_line(self, line):
        """
        add line to subway system
        :param line: a line object
        """
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
        assert len(path) >= 1

        ans = [[path[0], None]]
        if len(path) == 1:
            return ans

        now_line = self.get_edge_belongs(path[0].name, path[1].name)
        for i in range(1, len(path) - 1):
            nex_line = self.get_edge_belongs(path[i].name, path[i + 1].name)
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
        dist, last_st = {}, {}
        if isinstance(start, str):
            start = self.str2st[start]
        if isinstance(end, str):
            end = self.str2st[end]
        for station in self.nexto:
            dist[station] = INF
            last_st[station] = station

        # str as key
        queue = [start.name]
        head, tail = 0, 0

        # Station name
        dist[start.name] = 0
        while head <= tail:
            now_st = queue[head]
            head += 1
            for nex_ed in self.nexto[now_st.name]:
                nex_st = nex_ed.station_to
                if dist[nex_st] > dist[now_st] + 1:
                    if dist[nex_st] == INF:
                        tail += 1
                        queue.append(nex_st)
                    dist[nex_st] = dist[now_st] + 1
                    last_st[nex_st] = now_st

        path = []
        now_st = end.name
        while last_st[now_st] != now_st:
            path.append(self.str2st[now_st])
            now_st = last_st[now_st]
        path.append(self.str2st[now_st])
        path.reverse()
        return self._decorate_path(path)

    def _link(self, st_i, st_j):
        """
        create an edge between station i and station j
        :param st_i: a station object
        :param st_j: a station object
        """
        if st_i.name not in self.str2st.keys():
            self.str2st[st_i.name] = Station(st_i.name, st_i.is_trans)
        if st_j.name not in self.str2st.keys():
            self.str2st[st_j.name] = Station(st_j.name, st_j.is_trans)

        st_i = self.str2st[st_i.name]
        st_j = self.str2st[st_j.name]

        if st_i.name not in self.nexto:
            self.nexto[st_i.name] = []
        if st_j.name not in self.nexto:
            self.nexto[st_j.name] = []

        if not self.is_next(st_i_name=st_j.name, st_j_name=st_i.name):
            self.nexto[st_j.name].append(Edge(station_to=st_i.name, belong_to=edge_belong))
        if not self.is_next(st_i_name=st_i.name, st_j_name=st_j.name):
            self.nexto[st_i.name].append(Edge(station_to=st_j.name, belong_to=edge_belong))

    def test_by_file(self, file_path):
        """
        test all subways by file of path
        :param file_path:
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
                if (
                        test_line[index] not in self.str2st
                        or test_line[index + 1] not in self.str2st
                ):
                    print("error")
                    return
                # 已访问的站点
                if test_line[index] not in visited:
                    visited.append(test_line[index])
                if test_line[index + 1] not in visited:
                    visited.append(test_line[index + 1])
                st_i = self.str2st[test_line[index]]
                st_j = self.str2st[test_line[index + 1]]

                if st_i not in self.nexto[st_j]:
                    print("error! 不合理的站点连接: " + test_line[index] + " " + test_line[index + 1])
                    return

        for name in self.str2st.keys():
            if str(name) not in visited:
                print("false! 未访问的站点: " + str(name))

        # print("true!")
