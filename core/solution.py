"""solution"""

INF: int = 10000


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
