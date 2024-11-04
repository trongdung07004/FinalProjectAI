# import pygame
# import random
# import numpy as np
# from collections import deque
# import math
# import copy


# class GameAI:
#     def __init__(self):
#         pygame.init()
#         self.win = pygame.display.set_mode((1200, 800))
#         pygame.display.set_caption("Game AI")
#         self.fps = pygame.time.Clock()
#         self.font = pygame.font.Font(None, 36)

#         self.menu = True
#         self.createMap = False
#         self.isDragging = False
#         self.mouseThroughRect = []
#         self.rectMenu = [
#             pygame.Rect(500, 100, 200, 100),
#             pygame.Rect(500, 300, 200, 100),
#             pygame.Rect(500, 500, 200, 100),
#         ]
#         self.textMenu = ["Start", "Create Map", "Exit"]
#         self.textCreateMap = [
#             "Press and drag the mouse to",
#             "select the region",
#             "after selected a region",
#             "Press 1 to set the start position",
#             "Press 2 to set the end position",
#             "Press 3 to create a wall",
#             "Press 4 to delete",
#         ]
#         self.sizeMap = [29, 29]
#         self.rectMap = []
#         self.running = True
#         self.time = 0
#         self.start = False
#         self.end = False
#         self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
#         self.sizeImage = [27, 27]
#         self.posStart = [5, 5]
#         self.posEnd = [26, 19]
#         self.movePlayer = 0
#         self.player = [5, 5]
#         self.textPlayer = "Player"
#         self.vec = [0, 0]
#         self.playerFinish = False
#         self.info = {
#             # "dfs": [
#             #     [],
#             #     0,
#             #     False,
#             #     pygame.transform.scale(
#             #         pygame.image.load("images/dfs.png"),
#             #         (self.sizeImage[0], self.sizeImage[1]),
#             #     ),
#             #     (255, 0, 0),
#             #     pygame.rect.Rect(870, 1 * 100 + 150, 20, 20),
#             #     False,
#             #     "Dfs",
#             # ],
#             # "bfs": [
#             #     [],
#             #     0,
#             #     False,
#             #     pygame.transform.scale(
#             #         pygame.image.load("images/bfs.png"),
#             #         (self.sizeImage[0], self.sizeImage[1]),
#             #     ),
#             #     (255, 0, 0),
#             #     pygame.rect.Rect(870, 2 * 100 + 150, 20, 20),
#             #     False,
#             #     "Bfs",
#             # ],
#             # "greedy": [[], 0, False, pygame.transform.scale(pygame.image.load("images/greedy.png"), (self.sizeImage[0], self.sizeImage[1])), (255, 0, 0), pygame.rect.Rect(870, 3*100 + 150, 20, 20), False, "Greedy"],
#             # "aStar": [
#             #     [],
#             #     0,
#             #     False,
#             #     pygame.transform.scale(
#             #         pygame.image.load("images/hillclimbing.png"),
#             #         (self.sizeImage[0], self.sizeImage[1]),
#             #     ),
#             #     (255, 0, 0),
#             #     pygame.rect.Rect(870, 4 * 100 + 150, 20, 20),
#             #     False,
#             #     "Hill Climbing",
#             # ],
#             "aStar": [
#                 [],
#                 0,
#                 False,
#                 pygame.transform.scale(
#                     pygame.image.load("images/astar.png"),
#                     (self.sizeImage[0], self.sizeImage[1]),
#                 ),
#                 (255, 0, 0),
#                 pygame.rect.Rect(870, 5 * 100 + 150, 20, 20),
#                 False,
#                 "A*",
#             ]
#         }
#         self.intersections = []
#         self.dx = 45
#         self.dy = 10
#         self.images = [
#             pygame.transform.scale(
#                 pygame.image.load("images/finish.png"),
#                 (self.sizeImage[0], self.sizeImage[1]),
#             ),
#             pygame.transform.scale(
#                 pygame.image.load("images/10.png"),
#                 (self.sizeImage[0], self.sizeImage[1]),
#             ),
#             pygame.transform.scale(
#                 pygame.image.load("images/player.png"),
#                 (self.sizeImage[0], self.sizeImage[1]),
#             ),
#             pygame.transform.scale(pygame.image.load("images/bg.png"), (1220, 800)),
#         ]

#     # Algorithm
#     def Heuristic(self, current):
#         return abs(current[0] - self.posEnd[0]) + abs(current[1] - self.posEnd[1])

#     def FindIntersectionAStar(self, current, visited):
#         moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
#         temp = []
#         tempVisited = copy.deepcopy(visited)
#         for d in moves:
#             x, y = current[0] + d[0], current[1] + d[1]
#             if (
#                 0 <= x < self.sizeMap[0]
#                 and 0 <= y < self.sizeMap[1]
#                 and (x, y) not in tempVisited
#                 and self.map[x][y] == 0
#             ):
#                 temp.append([x, y])
#                 tempVisited.add(tuple([x, y]))

#         intersection = None
#         for i in temp:

#             path = [i]
#             count = None
#             while count != 0:
#                 x, y = path[-1]
#                 count = 0
#                 a = None

#                 for d in moves:
#                     nx, ny = x + d[0], y + d[1]

#                     if (
#                         0 <= nx < self.sizeMap[0]
#                         and 0 <= ny < self.sizeMap[1]
#                         and (nx, ny) not in tempVisited
#                         and self.map[nx][ny] == 0
#                     ):
#                         if [nx, ny] == self.posEnd:
#                             return [[nx, ny], 0, path[:]]
#                         count += 1
#                         a = [nx, ny]

#                 if count >= 2:
#                     heuristic = self.Heuristic([x, y])
#                     if intersection is None or (
#                         heuristic + len(path) < intersection[1]
#                     ):
#                         intersection = [[x, y], heuristic + len(path), path[:]]
#                     break
#                 elif count == 1:
#                     path.append(a)
#                     tempVisited.add(tuple(a))

#         return intersection

#     def AStar(self):
#         visited = set()
#         visited.add(tuple(self.posStart))
#         current = self.posStart
#         self.info["aStar"][0].append(tuple(current))
#         self.intersections.append(tuple(current))
#         while True:
#             a = self.FindIntersectionAStar(current, visited)
#             if a is None:
#                 while self.intersections[-1] != self.info["aStar"][0][-1]:
#                     self.info["aStar"][0].pop()
#                 current = self.info["aStar"][0].pop()
#                 self.intersections.pop()
#                 continue
#             elif a[1] == 0:
#                 for i in a[2]:
#                     self.info["aStar"][0].append(tuple(i))
#                 self.info["aStar"][0].append(tuple(self.posEnd))
#                 return
#             else:
#                 self.intersections.append(tuple(a[0]))
#                 current = a[0]
#                 for i in a[2]:
#                     self.info["aStar"][0].append(tuple(i))
#                     visited.add(tuple(i))

#     ## Stactic Display
#     def CreateMap(self):
#         moves = [(0, -2), (-2, 0), (0, 2), (2, 0)]
#         stack = []
#         self.map[self.posStart[0]][self.posStart[1]] = 0
#         self.map[self.posEnd[0]][self.posEnd[1]] = 0
#         random.shuffle(moves)
#         for dx, dy in moves:
#             nx, ny = self.posStart[0] + dx, self.posStart[1] + dy
#             if 1 <= nx < self.sizeMap[0] - 1 and 1 <= ny < self.sizeMap[1] - 1:
#                 self.map[nx][ny] = 0
#                 self.map[self.posStart[0] + dx // 2][self.posStart[1] + dy // 2] = 0
#                 stack.append([nx, ny])

#         self.map[self.posStart[0] + 3][self.posStart[1]] = 0
#         self.map[self.posStart[0] - 3][self.posStart[1]] = 0

#         while stack:
#             random.shuffle(moves)
#             random.shuffle(moves)
#             x, y = stack[-1]
#             for i in moves:
#                 nx, ny = x + i[0], y + i[1]
#                 if nx == self.posEnd[0] and ny == self.posEnd[1]:
#                     return

#                 if (
#                     1 <= nx < self.sizeMap[0] - 1
#                     and 1 <= ny < self.sizeMap[1] - 1
#                     and self.map[nx][ny] == 1
#                 ):
#                     self.map[nx][ny] = 0
#                     self.map[x + (i[0] // 2)][y + (i[1] // 2)] = 0
#                     stack.append([nx, ny])
#                     break
#             else:
#                 stack.pop()

#     def DrawMap(self):
#         pygame.draw.rect(
#             self.win,
#             (10, 10, 10),
#             (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 800),
#             2,
#             5,
#         )
#         for i in range(0, self.sizeMap[0]):
#             for j in range(0, self.sizeMap[1]):
#                 if self.map[i][j] == 1:
#                     self.win.blit(
#                         self.images[1],
#                         (
#                             j * self.sizeImage[0] + self.dx,
#                             i * self.sizeImage[1] + self.dy,
#                         ),
#                     )
#                 else:
#                     pygame.draw.rect(
#                         self.win,
#                         (0, 0, 0),
#                         pygame.rect.Rect(
#                             j * self.sizeImage[0] + self.dx,
#                             i * self.sizeImage[1] + self.dy,
#                             self.sizeImage[0],
#                             self.sizeImage[1],
#                         ),
#                         1,
#                         3,
#                     )

#         self.win.blit(
#             self.images[0],
#             (
#                 self.posEnd[1] * self.sizeImage[0] + self.dx,
#                 self.posEnd[0] * self.sizeImage[1] + self.dy,
#             ),
#         )

#     def DrawBot(self):
#         for i, j in self.info.items():
#             self.win.blit(
#                 j[3],
#                 (
#                     j[0][j[1]][1] * self.sizeImage[0] + self.dx,
#                     j[0][j[1]][0] * self.sizeImage[1] + self.dy,
#                 ),
#             )

#     def MoveBots(self):
#         for i, j in self.info.items():
#             if (
#                 not self.info[i][2]
#                 and self.info[i][6]
#                 and self.time % 10 == 0
#                 and self.info[i][1] < len(self.info[i][0]) - 1
#             ):
#                 self.info[i][1] += 1

#     def Run(self):
#         while self.running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#             self.win.fill((255, 255, 255))
#             self.DrawMap()
#             self.MoveBots()
#             self.DrawBot()
#             pygame.display.update()
#             self.fps.tick(60)
#             self.time += 1


# if "__main__" == __name__:
#     run = GameAI()
#     run.CreateMap()
#     run.AStar()
#     run.info["aStar"][2] = False
#     run.info["aStar"][6] = True
#     run.Run()


import pygame


def get_center_color(image_path):
    # Khởi tạo pygame
    pygame.init()

    # Tải ảnh bằng pygame
    img = pygame.image.load(image_path)

    # Lấy kích thước ảnh
    width, height = img.get_size()

    # Tính tọa độ trung tâm
    center_x = 15
    center_y = 15

    # Lấy màu tại điểm trung tâm
    center_color = img.get_at((center_x, center_y))[:3]

    # Kết thúc pygame
    pygame.quit()

    return center_color


# Sử dụng hàm
image_path = "images/ucs.png"  # Đường dẫn tới ảnh của bạn
center_color = get_center_color(image_path)
print("Màu tại trung tâm là:", center_color)
# while True:
#     if view:
#         mousePos = pygame.mouse.get_pos()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     return

#             if event.type == pygame.MOUSEBUTTONDOWN and temp is not None:
#                 for i in temp:
#                     if i[0].collidepoint(mousePos):
#                         self.RenderText()
#                         self.BotsColor()
#                         self.DrawMap()
#                         overlaySurface = pygame.Surface(
#                             self.sizeImage, pygame.SRCALPHA
#                         )
#                         pygame.draw.rect(self.win, (0, 0, 0), i[0], 2, 10)
#                         for x in self.allPath[i[1]][0]:
#                             pygame.draw.rect(
#                                 overlaySurface,
#                                 self.allPath[i[1]][1],
#                                 pygame.Rect(
#                                     0, 0, self.sizeImage[0], self.sizeImage[1]
#                                 ),
#                                 15,
#                                 5,
#                             )
#                             self.win.blit(
#                                 overlaySurface,
#                                 (
#                                     x[1] * self.sizeImage[0] + self.dx,
#                                     x[0] * self.sizeImage[1] + self.dy,
#                                 ),
#                             )
#                             pygame.display.update()
#                             pygame.time.delay(20)

#     else:
