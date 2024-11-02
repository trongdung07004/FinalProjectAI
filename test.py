# # import pygame
# # import random
# # import numpy as np
# # from collections import deque
# # import math
# # import copy


# # class GameAI:
# #     def __init__(self):
# #         pygame.init()
# #         self.win = pygame.display.set_mode((1200, 800))
# #         pygame.display.set_caption("Game AI")
# #         self.fps = pygame.time.Clock()
# #         self.font = pygame.font.Font(None, 36)

# #         self.menu = True
# #         self.createMap = False
# #         self.isDragging = False
# #         self.mouseThroughRect = []
# #         self.rectMenu = [
# #             pygame.Rect(500, 100, 200, 100),
# #             pygame.Rect(500, 300, 200, 100),
# #             pygame.Rect(500, 500, 200, 100),
# #         ]
# #         self.textMenu = ["Start", "Create Map", "Exit"]
# #         self.textCreateMap = [
# #             "Press and drag the mouse to",
# #             "select the region",
# #             "after selected a region",
# #             "Press 1 to set the start position",
# #             "Press 2 to set the end position",
# #             "Press 3 to create a wall",
# #             "Press 4 to delete",
# #         ]
# #         self.sizeMap = [29, 29]
# #         self.rectMap = []
# #         self.running = True
# #         self.time = 0
# #         self.start = False
# #         self.end = False
# #         self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
# #         self.sizeImage = [27, 27]
# #         self.posStart = [5, 5]
# #         self.posEnd = [26, 19]
# #         self.movePlayer = 0
# #         self.player = [5, 5]
# #         self.textPlayer = "Player"
# #         self.vec = [0, 0]
# #         self.playerFinish = False
# #         self.info = {
# #             # "dfs": [
# #             #     [],
# #             #     0,
# #             #     False,
# #             #     pygame.transform.scale(
# #             #         pygame.image.load("images/dfs.png"),
# #             #         (self.sizeImage[0], self.sizeImage[1]),
# #             #     ),
# #             #     (255, 0, 0),
# #             #     pygame.rect.Rect(870, 1 * 100 + 150, 20, 20),
# #             #     False,
# #             #     "Dfs",
# #             # ],
# #             # "bfs": [
# #             #     [],
# #             #     0,
# #             #     False,
# #             #     pygame.transform.scale(
# #             #         pygame.image.load("images/bfs.png"),
# #             #         (self.sizeImage[0], self.sizeImage[1]),
# #             #     ),
# #             #     (255, 0, 0),
# #             #     pygame.rect.Rect(870, 2 * 100 + 150, 20, 20),
# #             #     False,
# #             #     "Bfs",
# #             # ],
# #             # "greedy": [[], 0, False, pygame.transform.scale(pygame.image.load("images/greedy.png"), (self.sizeImage[0], self.sizeImage[1])), (255, 0, 0), pygame.rect.Rect(870, 3*100 + 150, 20, 20), False, "Greedy"],
# #             "hillclimbing": [
# #                 [],
# #                 0,
# #                 False,
# #                 pygame.transform.scale(
# #                     pygame.image.load("images/hillclimbing.png"),
# #                     (self.sizeImage[0], self.sizeImage[1]),
# #                 ),
# #                 (255, 0, 0),
# #                 pygame.rect.Rect(870, 4 * 100 + 150, 20, 20),
# #                 False,
# #                 "Hill Climbing",
# #             ],
# #             # "aStar": [[], 0, False, pygame.transform.scale(pygame.image.load("images/astar.png"), (self.sizeImage[0], self.sizeImage[1])), (255, 0, 0), pygame.rect.Rect(870, 5*100 + 150, 20, 20), False, "A*"]
# #         }

# #         self.dx = 45
# #         self.dy = 10
# #         self.images = [
# #             pygame.transform.scale(
# #                 pygame.image.load("images/finish.png"),
# #                 (self.sizeImage[0], self.sizeImage[1]),
# #             ),
# #             pygame.transform.scale(
# #                 pygame.image.load("images/10.png"),
# #                 (self.sizeImage[0], self.sizeImage[1]),
# #             ),
# #             pygame.transform.scale(
# #                 pygame.image.load("images/player.png"),
# #                 (self.sizeImage[0], self.sizeImage[1]),
# #             ),
# #             pygame.transform.scale(pygame.image.load("images/bg.png"), (1220, 800)),
# #         ]

# #     # Algorithm
# #     def Heuristic(self, current):
# #         return abs(current[0] - self.posEnd[0]) + abs(current[1] - self.posEnd[1])

# #     def FindIntersection(self, current, visited):
# #         moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
# #         temp = []

# #         for d in moves:
# #             x, y = current[0] + d[0], current[1] + d[1]
# #             if (
# #                 0 <= x < self.sizeMap[0]
# #                 and 0 <= y < self.sizeMap[1]
# #                 and (x, y) not in visited
# #                 and self.map[x][y] == 0
# #             ):
# #                 temp.append([x, y])
# #                 visited.add(tuple([x, y]))

# #         intersection = None

# #         for i in temp:
# #             path = [i]
# #             count = None

# #             while count != 0:
# #                 x, y = path[-1]
# #                 count = 0
# #                 a = None

# #                 for d in moves:
# #                     nx, ny = x + d[0], y + d[1]
# #                     if (
# #                         0 <= nx < self.sizeMap[0]
# #                         and 0 <= ny < self.sizeMap[1]
# #                         and (nx, ny) not in visited
# #                         and self.map[nx][ny] == 0
# #                     ):
# #                         if [nx, ny] == self.posEnd:
# #                             return [[nx, ny], 0, path[:]]
# #                         count += 1
# #                         a = [nx, ny]

# #                 if count >= 2:
# #                     heuristic = self.Heuristic([x, y])
# #                     if intersection is None or intersection[1] > heuristic:
# #                         intersection = [[x, y], heuristic, path[:]]
# #                     break
# #                 elif count == 1:
# #                     visited.add(tuple(a))
# #                     path.append(a)
# #         return intersection

# #     def Hillclimbing(self):
# #         visited = set()
# #         visited.add(tuple(self.posStart))
# #         current = self.posStart
# #         self.info["hillclimbing"][0].append(current)

# #         while True:
# #             a = self.FindIntersection(current, visited)
# #             if a is None:
# #                 return
# #             elif a[1] == 0:
# #                 for i in a[2]:
# #                     self.info["hillclimbing"][0].append(i)
# #                 self.info["hillclimbing"][0].append(self.posEnd)
# #                 print(a[1])
# #                 return
# #             print(a[1])
# #             current = a[0]
# #             for i in a[2]:
# #                 self.info["hillclimbing"][0].append(i)
# #             visited.add(tuple(current))

# #     ## Stactic Display
# #     def CreateMap(self):
# #         moves = [(0, -2), (-2, 0), (0, 2), (2, 0)]
# #         stack = []
# #         self.map[self.posStart[0]][self.posStart[1]] = 0
# #         self.map[self.posEnd[0]][self.posEnd[1]] = 0
# #         random.shuffle(moves)
# #         for dx, dy in moves:
# #             nx, ny = self.posStart[0] + dx, self.posStart[1] + dy
# #             if 1 <= nx < self.sizeMap[0] - 1 and 1 <= ny < self.sizeMap[1] - 1:
# #                 self.map[nx][ny] = 0
# #                 self.map[self.posStart[0] + dx // 2][self.posStart[1] + dy // 2] = 0
# #                 stack.append([nx, ny])

# #         self.map[self.posStart[0] + 3][self.posStart[1]] = 0
# #         self.map[self.posStart[0] - 3][self.posStart[1]] = 0

# #         while stack:
# #             random.shuffle(moves)
# #             random.shuffle(moves)
# #             x, y = stack[-1]
# #             for i in moves:
# #                 nx, ny = x + i[0], y + i[1]
# #                 if nx == self.posEnd[0] and ny == self.posEnd[1]:
# #                     return

# #                 if (
# #                     1 <= nx < self.sizeMap[0] - 1
# #                     and 1 <= ny < self.sizeMap[1] - 1
# #                     and self.map[nx][ny] == 1
# #                 ):
# #                     self.map[nx][ny] = 0
# #                     self.map[x + (i[0] // 2)][y + (i[1] // 2)] = 0
# #                     stack.append([nx, ny])
# #                     break
# #             else:
# #                 stack.pop()

# #     def DrawMap(self):
# #         pygame.draw.rect(
# #             self.win,
# #             (10, 10, 10),
# #             (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 800),
# #             2,
# #             5,
# #         )
# #         for i in range(0, self.sizeMap[0]):
# #             for j in range(0, self.sizeMap[1]):
# #                 if self.map[i][j] == 1:
# #                     self.win.blit(
# #                         self.images[1],
# #                         (
# #                             j * self.sizeImage[0] + self.dx,
# #                             i * self.sizeImage[1] + self.dy,
# #                         ),
# #                     )
# #                 else:
# #                     pygame.draw.rect(
# #                         self.win,
# #                         (0, 0, 0),
# #                         pygame.rect.Rect(
# #                             j * self.sizeImage[0] + self.dx,
# #                             i * self.sizeImage[1] + self.dy,
# #                             self.sizeImage[0],
# #                             self.sizeImage[1],
# #                         ),
# #                         1,
# #                         3,
# #                     )

# #         self.win.blit(
# #             self.images[0],
# #             (
# #                 self.posEnd[1] * self.sizeImage[0] + self.dx,
# #                 self.posEnd[0] * self.sizeImage[1] + self.dy,
# #             ),
# #         )

# #     def DrawBot(self):
# #         for i, j in self.info.items():
# #             self.win.blit(
# #                 j[3],
# #                 (
# #                     j[0][j[1]][1] * self.sizeImage[0] + self.dx,
# #                     j[0][j[1]][0] * self.sizeImage[1] + self.dy,
# #                 ),
# #             )

# #     def MoveBots(self):
# #         for i, j in self.info.items():
# #             if (
# #                 not self.info[i][2]
# #                 and self.info[i][6]
# #                 and self.time % 10 == 0
# #                 and self.info[i][1] < len(self.info[i][0]) - 1
# #             ):
# #                 self.info[i][1] += 1

# #     def Run(self):
# #         while self.running:
# #             for event in pygame.event.get():
# #                 if event.type == pygame.QUIT:
# #                     self.running = False

# #             self.win.fill((255, 255, 255))
# #             self.DrawMap()
# #             self.MoveBots()
# #             self.DrawBot()
# #             pygame.display.update()
# #             self.fps.tick(60)
# #             self.time += 1


# # if "__main__" == __name__:
# #     run = GameAI()
# #     run.CreateMap()
# #     run.Hillclimbing()
# #     run.info["hillclimbing"][2] = False
# #     run.info["hillclimbing"][6] = True
# #     run.Run()


# class MyClass:
#     def __init__(self, name):
#         self.name = name
#         print(f"Đã khởi tạo với tên: {self.name}")


# # Tạo đối tượng từ lớp
# obj = MyClass("ChatGPT")  # Lần đầu gọi __init__

# # Gọi lại __init__ với một giá trị mới
# obj.__init__("Python")  # Lần thứ hai gọi __init__
# print(obj.name)  # Output: Python

import pygame

# Khởi tạo Pygame
pygame.init()

# Danh sách đường dẫn đến các ảnh
image_paths = [
    "images/dfs.png",
    "images/bfs.png",
    "images/hillclimbing.png",
    "images/greedy.png",
    "images/astar.png",
]

# Tạo danh sách để lưu mã màu
colors = []

# Lặp qua từng ảnh, tải và lấy mã màu ở trung tâm
for path in image_paths:
    # Tải ảnh
    image = pygame.image.load(path)

    # Lấy kích thước ảnh và tính tọa độ trung tâm
    center_x = image.get_width() // 2
    center_y = image.get_height() // 2

    # Lấy mã màu tại vị trí trung tâm
    color = image.get_at((center_x, center_y))[:3]  # Chỉ lấy RGB

    # Thêm mã màu vào danh sách
    colors.append(color)

# Thoát Pygame
pygame.quit()

# In mã màu của từng ảnh
for i, color in enumerate(colors):
    print(f"Mã màu của ảnh {i + 1} (RGB): {color}")
