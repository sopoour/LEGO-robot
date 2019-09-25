from collections import deque

def main(graph, robotPos, robotDir, canPos, canGoal):
    path = planner(graph, canPos[0], canGoal[0])
    path2 = planner(graph, canPos[1], canGoal[1])

    robotGoal = int(canGoal[0]) - 8
    print("robot goal", robotGoal)
    robotGoal1 = str(robotGoal)
    print("robot goal2", robotGoal1)
    robotGoal2 = planner(graph, robotPos, robotGoal1)

    if path and path2:
        print(path)
        print(path2)
        print("robotgoal22", robotGoal2)

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
          if neighbour == goal:
              return path + [current, neighbour]
          if neighbour in visited:
              continue
          queue.append((neighbour, path + [current]))
          visited.add(neighbour)
    return None  #No path found


def checkIfValidMove(neighbour):
  if(neighbour == canPos):
    print("found can")




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
    canPos = ['5', '6']
    canGoal = ['10', '1']

    main(graph, robotPos, robotDir, canPos, canGoal)
