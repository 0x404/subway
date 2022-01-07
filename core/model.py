INF = 10000

class Station():
    """
    station class
    """
    def __init__(self, st_name, is_trans=False):
        self.station_name = st_name
        self.trans = is_trans

    @property
    def name(self):
        '''get station's name'''
        return self.station_name

    @property
    def is_trans(self):
        '''whther a station is a transfer station'''
        return self.trans

class Line():
    """
    line class, consists of stations
    """
    def __init__(self, line_name, st_list, is_ring=False):
        self.line_name = line_name
        self.st_list = st_list
        self.ring = is_ring

    @property
    def is_ring(self):
        '''whether the line is a ring'''
        return self.ring

    @property
    def station_list(self):
        '''get station list of a line'''
        return self.st_list

class SubwaySys():
    """
    subwaySys class, consists of lines
    """
    def __init__(self, line_list=None):
        self.str2st = {}
        self.nexto = {}
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
            dist[station] = INF
            last_st[station] = station

        queue = [0 for _ in range(len(self.nexto))]
        head, tail = 0, 0
        queue[0] = start
        dist[start] = 0

        while head <= tail:
            now_st = queue[head]
            head += 1
            for nex_st in self.nexto[now_st]:
                if dist[nex_st] > dist[now_st] + 1:
                    if dist[nex_st] == INF:
                        tail += 1
                        queue[tail] = nex_st
                    dist[nex_st] = dist[now_st] + 1
                    last_st[nex_st] = now_st

        path = []
        now_st = end
        while last_st[now_st] != now_st:
            path.append(now_st)
        path.append(now_st)
        return path
        # return reversed(path)

    def _link(self, st_i, st_j):
        """
        create an edge between station i and station j
        :param st_i: a station obejct
        :param st_j: a station object
        """
        if st_i not in self.nexto.keys():
            self.str2st[st_i.station_name] = st_i
            self.nexto[st_i] = []
        if st_j not in self.nexto.keys():
            self.str2st[st_j.station_name] = st_j
            self.nexto[st_j] = []
        if st_i not in self.nexto[st_j]:
            self.nexto[st_j].append(st_i)
        if st_j not in self.nexto[st_i]:
            self.nexto[st_i].append(st_j)
