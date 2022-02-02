"""solution"""
INF: int = 10000


def get_line_belong(st_i, st_j, nexto):
    """Get line belong.

    Get the name of line that connect station i and station j.

    Args:
        st_i: str, station name.
        st_j: str, station name.
        nexto: map, adjacency table of subway system.

    Return:
        the line name of edge(station i, station j).
    """
    assert st_i in nexto, "station don't exist."
    assert st_j in nexto, "station don't exist."

    for edge in nexto[st_j]:
        if edge.station_to == st_i:
            return edge.belong_to
    for edge in nexto[st_i]:
        if edge.station_to == st_j:
            return edge.belong_to
    raise Exception("{} and {} are not adjacent.".format(st_i, st_j))


def is_nexto(st_i, st_j, nexto):
    """Whther station i is next to station j.

    Args:
        st_i: str, station name.
        st_j: str, station name.
        nexto: map, adjacency table of subway system.

    Return:
        True: if station i is next to station j.
        False: ohterwise.
    """
    assert st_i in nexto, "station don't exist."
    assert st_j in nexto, "station don't exist."

    for edge in nexto[st_j]:
        if edge.station_to == st_i:
            return True
    return False


def docorate_path(path, nexto):
    """Decorate path.

    Decorate station list into station with message.

    Args:
        path: station list, e.g. [station1, station2, station3]
        nexto: map, adjacency table of subway system.

    Return:
        list: [[station1, msg1], [station2, msg2], [station3, msg3]].
        station: station instance.
        msg: str or None.
    """
    assert len(path) >= 1, "path to be decorated is empty."
    ans = [[path[0], None]]
    if len(path) == 1:
        return ans

    now_line = get_line_belong(path[0].name, path[1].name, nexto)
    for i in range(1, len(path) - 1):
        nex_line = get_line_belong(path[i].name, path[i + 1].name, nexto)
        if now_line != nex_line:
            ans.append([path[i], "换乘" + nex_line])
            now_line = nex_line
        else:
            ans.append([path[i], None])
    ans.append([path[-1], None])
    return ans


def shortest_path(start, end, nexto):
    """Calculate the shortest path.

    Calculate the shortest path form start station to end station.

    Args:
        start: str, the name of start station.
        end: str, the name of end station.
        nexto: map, adjacency table of subway system.

    Return:
        A list of station name indicate the path.
    """
    dist, last_st = {}, {}
    for station in nexto:
        dist[station] = INF
        last_st[station] = station

    queue = [start]
    dist[start] = 0
    head, tail = 0, 0
    while head <= tail:
        now_st = queue[head]
        if now_st == end:
            break
        head += 1
        for nex_ed in nexto[now_st]:
            nex_st = nex_ed.station_to
            if dist[nex_st] > dist[now_st] + 1:
                if dist[nex_st] == INF:
                    tail += 1
                    queue.append(nex_st)
                dist[nex_st] = dist[now_st] + 1
                last_st[nex_st] = now_st

    path = []
    now_st = end
    while last_st[now_st] != now_st:
        path.append(now_st)
        now_st = last_st[now_st]
    path.append(now_st)
    path.reverse()
    return path


def travel_path_from(start, nexto, lines):
    """Get travel path.

    Calculate the path that travels every station in subway system from `start` station.

    Args:
        start: str, the name of start station.
        nexto: map, adjacency table of subway system.
        lines: list, e.g. [line1, line2, ...].

    Return:
        A list of station name indicates the path.
    """
    ans = []
    cur_start = start
    visited = {line.name: False for line in lines}

    for _ in range(len(lines)):
        min_cost = INF
        for line in lines:
            if visited[line.name]:
                continue

            path = shortest_path(cur_start, line.start, nexto)
            station_list = [st.name for st in line.station_list]
            path = path + station_list[1:]
            if len(path) < min_cost:
                min_cost = len(path)
                nex_start = line.end
                traveled_line = line.name
                traveled_path = path[:]

            path = shortest_path(cur_start, line.end, nexto)
            station_list = [st.name for st in line.station_list]
            path = path + station_list[line.length - 2 :: -1]
            if len(path) < min_cost:
                min_cost = len(path)
                nex_start = line.start
                traveled_line = line.name
                traveled_path = path[:]

        if len(ans) > 0 and ans[-1] == traveled_path[0]:
            ans = ans + traveled_path[1:]
        else:
            ans = ans + traveled_path

        cur_start = nex_start
        visited[traveled_line] = True
    return ans


def verify_path(path):
    """Verify path

    Args:
        path: station str list.

    Return:
        True: If the stations in the list do cover all stations of the whole subway at least once,
              and the number of stations is correct, the traversal order of stations is reasonable.
        False: The traversal order of stations is still reasonable, but there are missing stations
               or the number of stations is wrong. If there are missing stations,
               this program should output at least one missing station name.
        Error: If the traversal order of the station is unreasonable
    """
    # Subwaysys.test_by_file should be refactored and moved here.
    pass
