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

    @property
    def belong(self):
        """which line a station belong to"""
        return self.belong_to


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

    def add_line(self, line):
        """
        add line to subway system
        :param line: a line object
        """
        for i in range(len(line.station_list) - 1):
            self._link(line.station_list[i], line.station_list[i + 1])
        if line.is_ring and len(line.station_list) > 1:
            self._link(line.station_list[0], line.station_list[-1])

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
        for station in self.nexto.keys():
            dist[station.name] = INF
            last_st[station.name] = station.name

        queue = [start]
        head, tail = 0, 0
        dist[start.name] = 0
        while head <= tail:
            now_st = queue[head]
            head += 1
            for nex_st in self.nexto[now_st]:
                if dist[nex_st.name] > dist[now_st.name] + 1:
                    if dist[nex_st.name] == INF:
                        tail += 1
                        queue.append(nex_st)
                    dist[nex_st.name] = dist[now_st.name] + 1
                    last_st[nex_st.name] = now_st.name

        path = []
        now_st = end.name
        while last_st[now_st] != now_st:
            path.append(self.str2st[now_st])
            now_st = last_st[now_st]
        path.append(self.str2st[now_st])
        path.reverse()
        return path

    def _link(self, st_i, st_j):
        """
        create an edge between station i and station j
        :param st_i: a station obejct
        :param st_j: a station object
        """
        if st_i.name not in self.str2st.keys():
            self.str2st[st_i.name] = Station(st_i.name, st_i.is_trans)
        if st_j.name not in self.str2st.keys():
            self.str2st[st_j.name] = Station(st_j.name, st_j.is_trans)

        st_i = self.str2st[st_i.name]
        st_j = self.str2st[st_j.name]
        if st_i not in self.nexto.keys():
            self.nexto[st_i] = []
        if st_j not in self.nexto.keys():
            self.nexto[st_j] = []
        if st_i not in self.nexto[st_j]:
            self.nexto[st_j].append(st_i)
        if st_j not in self.nexto[st_i]:
            self.nexto[st_i].append(st_j)

    def get_station_number(self):
        return len(self.str2st)

    def test_by_file(self,file_path):
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
            for index in range(len(test_line)-1):
                if test_line[index] not in self.str2st.keys() or test_line[index + 1] not in self.str2st.keys():
                    print('error')
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
