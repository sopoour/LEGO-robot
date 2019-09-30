from collections import deque

def main(graph, robotPos, canPos, canGoal):
    path = planner(graph, canPos[0], canGoal[0])
    robotGoTo = robotPathToCan(graph, path, robotPos[0])
    robotPos[0] = path[len(path)-2]
    print("Robot pos: ", robotPos)
    finalPath = robotGoTo + path + robotPos

    if path:
        print("The path is: ", finalPath)

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
        print("neighbour: ",neighbour)
        #if(checkIfValidMove(neighbour)):
        if neighbour != canPos[0] and neighbour != canPos[1]:
          if neighbour == goal:
              canPos[0] = goal
              return path + [current, neighbour]
          if neighbour in visited:
              continue
          queue.append((neighbour, path + [current]))
          visited.add(neighbour)
  return None  #No path found


def robotPathToCan(graph, path, robotPos):
    if(path[0] - path[1]) == 4:
      robotGoTo = planner(graph, robotPos, path[0] + 4)
    elif(path[0] - path[1] == -4):
      robotGoTo = planner(graph, robotPos, path[0] - 4)
    elif(path[0] - path[1] == 1):
      robotGoTo = planner(graph, robotPos, path[0] + 1)
    elif(path[0] - path[1] == -1):
      robotGoTo = planner(graph, robotPos, path[0] -1)
    return robotGoTo

if __name__ == '__main__':
    graph = {
        0: [1, 4],
        1: [0, 2, 5],
        2: [1, 3, 6],
        3: [2, 7],
        4: [0, 5, 8],
        5: [1, 4, 6, 9],
        6: [2, 5, 7, 10],
        7: [3, 6, 11],
        8: [4, 9, 12],
        9: [5, 8, 10, 13],
        10: [6, 9, 11, 14],
        11: [7, 10, 15],
        12: [8, 13],
        13: [9, 12, 14],
        14: [10, 13, 15],
        15: [11, 14],
        }

    robotPos = [13]
    canPos = [10, 1]
    canGoal = [6, 2]

    main(graph, robotPos, canPos, canGoal)
