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
        return solution.docorate_path(ans_path, self.nexto)

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

    def _link(self, st_i, st_j, edge_belong, directed=False):
        """Link station i and station j in subway system.

        Args:
            st_i: station object.
            st_j: station object.
            edge_belong: str, line name of Edge(station i, station j).
            directed: bool, indicates whether it is directed.

        Return:
            None.
        """
        if st_i.name not in self.str2st:
            self.str2st[st_i.name] = Station(st_i.name, st_i.is_trans)
        if st_j.name not in self.str2st:
            self.str2st[st_j.name] = Station(st_j.name, st_j.is_trans)

        st_i = st_i.name
        st_j = st_j.name

        if st_i not in self.nexto:
            self.nexto[st_i] = []
        if st_j not in self.nexto:
            self.nexto[st_j] = []

        if not solution.is_nexto(st_j, st_i, self.nexto):
            self.nexto[st_i].append(Edge(st_j, edge_belong))

        if not directed and not solution.is_nexto(st_i, st_j, self.nexto):
            self.nexto[st_j].append(Edge(st_i, edge_belong))
