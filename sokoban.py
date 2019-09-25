from collections import deque

def main(graph, robotPos, robotDir, canPos, canGoal):
    path = planner(graph, robotPos, canPos)

    if path:
        print(path)

    else:
        print('no path found')

def planner(graph, start, goal):
    if start == goal:
        return [start]
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        visited.add(current)
        for neighbour in graph[current]:
            if(checkIfValidMove(graph[current], neighbour))
              if neighbour == goal:
                  return path + [current, neighbour]
              if neighbour in visited:
                  continue
              queue.append((neighbour, path + [current]))
              visited.add(neighbour)
    return None  #No path found


def checkIfValidMove(current, neighbour):




if __name__ == '__main__':
    graph = {
        '0': ['1', '4'],
        '1': ['0', '2', '5'],
        '2': ['1', '3', '6'],
        '3': ['2', '7'],
        '4': ['0', '5', '8'],
        '5': ['1', '4', '6', '9'],
        '6': ['2', '5', '7', '10'],
        '7': ['3', '6', '11'],
        '8': ['4', '9', '12'],
        '9': ['5', '8', '10', '13'],
        '10': ['6', '9', '11', '14'],
        '11': ['7', '10', '15'],
        '12': ['8', '13'],
        '13': ['9', '12', '14'],
        '14': ['10', '13', '15'],
        '15': ['11', '14'],
        }

    robotPos = '1'
    robotDir = '0'
    canPos = '6'
    canGoal = '10'
