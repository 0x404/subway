'''model'''
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


class Edge:
    """
    line edge
    :param st_j(Station)    : Edge visited station
    :param line_belongs(str): this edge belongs which line
    """

    def __init__(self, st_j, line_belongs):
        self.st_j = st_j
        self.line_belongs = line_belongs

    @property
    def vis_station(self):
        """which station an edge link to"""
        return self.st_j

    @property
    def lines_belongs(self):
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
    def is_ring(self):
        """whether the line is a ring"""
        return self.ring

    @property
    def station_list(self):
        """get station list of a line"""
        return self.st_list


class SubwaySys:
    """
    subwaySys class, consists of lines
    """

    def __init__(self, line_list=None):
        self.str2st = {}  # station_name -> station
        self.nexto = {}  # station -> station_list
        if line_list is not None:
            for line in line_list:
                self.add_line(line)

    def get_edge_belongs(self, st_i, st_j):
        """
        :param st_i: station name one
        :param st_j: station name two
        :return: line_name
        """
        if isinstance(st_i, str):
            st_i = self.str2st[st_i]
        if isinstance(st_j, str):
            st_j = self.str2st[st_j]

        for nxt_ed in self.nexto[st_i]:
            if nxt_ed.vis_station() == st_j:
                return nxt_ed.lines_belongs()
        return "null??"

    def add_line(self, line):
        """
        add line to subway system
        :param line: a line object
        """
        for i in range(len(line.station_list) - 1):
            self._link(line.station_list[i], line.station_list[i + 1], line.line_name)
        if line.is_ring and len(line.station_list) > 1:
            self._link(line.station_list[0], line.station_list[-1], line.line_name)

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
            dist[station.name] = INF
            last_st[station.name] = station.name

        queue = [start]
        head, tail = 0, 0
        dist[start.name] = 0
        while head <= tail:
            now_st = queue[head]
            head += 1
            for nex_ed in self.nexto[now_st]:
                nex_st = nex_ed.vis_station()
                if dist[nex_st.name] > dist[now_st.name] + 1:
                    if dist[nex_st.name] == INF:
                        tail += 1
                        queue.append(nex_st)
                    dist[nex_st.name] = dist[now_st.name] + 1
                    last_st[nex_st.name] = now_st.name

        path = []
        now_st = end.name
        while last_st[now_st] != now_st:
            print(
                str(now_st)
                + "  "
                + str(last_st[now_st])
                + " "
                + self.get_edge_belongs(now_st, last_st[now_st])
            )
            path.append(self.str2st[now_st])
            now_st = last_st[now_st]
        path.append(self.str2st[now_st])
        path.reverse()
        return path

    def _link(self, st_i, st_j, edge_belong):
        """
        create an edge between station i and station j
        :param st_i: a station obejct
        :param st_j: a station object
        """
        if st_i.name not in self.str2st:
            self.str2st[st_i.name] = Station(st_i.name, st_i.is_trans)
        if st_j.name not in self.str2st:
            self.str2st[st_j.name] = Station(st_j.name, st_j.is_trans)

        st_i = self.str2st[st_i.name]
        st_j = self.str2st[st_j.name]
        if st_i not in self.nexto.keys():
            self.nexto[st_i] = []
        if st_j not in self.nexto.keys():
            self.nexto[st_j] = []
        if st_i not in self.nexto[st_j]:
            self.nexto[st_j].append(Edge(st_i, edge_belong))
        if st_j not in self.nexto[st_i]:
            self.nexto[st_i].append(Edge(st_j, edge_belong))

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

            # 当前线路是否连接合法个
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
