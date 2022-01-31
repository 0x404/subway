"""solution"""
INF: int = 10000


def shortest_path(start, end, nexto):
    """Calculate the shortest path.

    Calculate the shortest path form start station to end station.

    Args:
        start: the name of start station.
        end: the name of end station.
        nexto: adjacency table of subway system.

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
