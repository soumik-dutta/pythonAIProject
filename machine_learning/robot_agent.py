import random
from collections import deque


def initialize_warehouse(N, M, P, O, seed=2):
    random.seed(seed)
    warehouse = [['.' for _ in range(M)] for _ in range(N)]

    # Place obstacles
    obstacles = set()
    while len(obstacles) < O:
        x, y = random.randint(0, N - 1), random.randint(0, M - 1)
        if (x, y) not in obstacles:
            obstacles.add((x, y))
            warehouse[x][y] = 'X'

    # Place packages and drop-offs
    packages, drop_offs = [], []
    while len(packages) < P:
        px, py = random.randint(0, N - 1), random.randint(0, M - 1)
        dx, dy = random.randint(0, N - 1), random.randint(0, M - 1)
        if ((px, py) not in obstacles and
                (dx, dy) not in obstacles and
                (px, py) != (dx, dy) and
                ((px, py) not in drop_offs and (dx, dy) not in packages)):
            packages.append((px, py))
            drop_offs.append((dx, dy))
            warehouse[px][py] = 'P'
            warehouse[dx][dy] = 'D'

    # Set robot start position
    while True:
        sx, sy = random.randint(0, N - 1), random.randint(0, M - 1)
        if (sx, sy) not in obstacles and (sx, sy) not in packages and (sx, sy) not in drop_offs:
            warehouse[sx][sy] = 'R'
            break

    return warehouse, (sx, sy), packages, drop_offs, obstacles


def print_warehouse(warehouse):
    for row in warehouse:
        print(" ".join(row))
    print()


def bfs(start, goal, warehouse, obstacles):
    N, M = len(warehouse), len(warehouse[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Up, Left, Down
    queue = deque([(start, [])])
    visited = set()
    penalty = 0

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path + [(x, y)], penalty

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < M and (nx, ny) not in visited:
                if warehouse[nx][ny] != 'X':
                    queue.append(((nx, ny), path + [(x, y)]))
                else:
                    penalty += 1
    return []  # No path found


def robot_agent(N, M, P, O, seed=42):
    warehouse, start, packages, drop_offs, obstacles = initialize_warehouse(N, M, P, O, seed)
    print("Initial Warehouse Configuration:")
    print_warehouse(warehouse)

    robot_position = start
    total_cost, total_reward, penalty = 0, 0, 0

    for package, drop_off in zip(packages, drop_offs):
        # Move to package
        path_to_package, penalty = bfs(robot_position, package, warehouse, obstacles)
        if path_to_package:
            total_cost += len(path_to_package) - 1
            robot_position = package

        # Move to drop-off
        path_to_dropoff, penalty = bfs(robot_position, drop_off, warehouse, obstacles)
        if path_to_dropoff:
            total_cost += len(path_to_dropoff) - 1
            robot_position = drop_off
            total_reward += 10  # Successful delivery

    total_reward = total_reward - (penalty * 5)
    final_score = total_reward - total_cost

    print("Final Score:", final_score)
    print("Total Cost:", total_cost)
    print("Total Reward:", total_reward)
    print("Penalty cost: ", penalty, "seed value: ", seed)
    print(f'Obstacles: {obstacles}\nPackages: {packages}\nDrop-offs: {drop_offs}\n')


if __name__ == '__main__':
    package = random.randint(2, 6)
    obstacle = random.randint(1, 10)
    n = random.randint(5, 10)
    m = random.randint(5, 10)
    robot_agent(N=n, M=m, P=package, O=obstacle, seed=42)
