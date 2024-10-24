import pygame
import random
import numpy as np
from collections import deque

class GameAI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1200, 870))
        pygame.display.set_caption("Game AI")
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.text = ["Player: ", "Dfs: ", "Bfs: "]
        self.time = 0
        self.sizeMap = [29, 29]
        self.running = True
        self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
        self.sizeImage = [30, 30]
        self.posStart = [5, 5]
        self.posEnd = [27, 20]
        self.player = [5, 5]
        self.vec = [0, 0]
        self.playerFinish = False
        self.finished = 1
        self.info = {
            "dfs": [[], 0, False, pygame.transform.scale(pygame.image.load("images/dfs.png"), (self.sizeImage[0], self.sizeImage[1]))],
            "bfs": [[], 0, False,  pygame.transform.scale(pygame.image.load("images/bfs.png"), (self.sizeImage[0], self.sizeImage[1]))],
            #"greendy": [[], 0, False,  pygame.transform.scale(pygame.image.load("images/bfs.png"), (self.sizeImage[0], self.sizeImage[1]))],
            }
        self.dx = 65
        self.dy = 0
        self.images = [
            pygame.transform.scale(pygame.image.load("images/finish.png"), (self.sizeImage[0], self.sizeImage[1])),
            pygame.transform.scale(pygame.image.load("images/10.png"), (self.sizeImage[0], self.sizeImage[1])),
            pygame.transform.scale(pygame.image.load("images/player.png"), (self.sizeImage[0], self.sizeImage[1])),
        ]

    def CreateMap(self):
        moves = [(0, -2), (-2, 0), (0, 2), (2, 0)]
        stack = []
        self.map[self.posStart[0]][self.posStart[1]] = 0
        self.map[self.posEnd[0]][self.posEnd[1]] = 0
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = self.posStart[0] + dx, self.posStart[1] + dy
            if 1 <= nx < self.sizeMap[0] - 1 and 1 <= ny < self.sizeMap[1] - 1:
                self.map[nx][ny] = 0
                self.map[self.posStart[0] + dx // 2][self.posStart[1] + dy // 2] = 0
                stack.append([nx, ny])

        self.map[self.posStart[0] + 3][self.posStart[1]] = 0
        self.map[self.posStart[0] - 3][self.posStart[1]] = 0

        while stack:
            random.shuffle(moves)
            random.shuffle(moves)
            x, y = stack[-1]
            for i in moves:
                nx, ny = x + i[0], y + i[1]
                if nx == self.posEnd[0] and ny == self.posEnd[1]:
                    return

                if 1 <= nx < self.sizeMap[0] - 1 and 1 <= ny < self.sizeMap[1] - 1 and self.map[nx][ny] == 1:
                    self.map[nx][ny] = 0
                    self.map[x + (i[0] // 2)][y + (i[1] // 2)] = 0
                    stack.append([nx, ny])
                    break
            else:
                stack.pop()

    def DrawMap(self):
        for i in range(0, self.sizeMap[0]):
            for j in range(0, self.sizeMap[1]):
                if self.map[i][j] == 1:
                    self.win.blit(self.images[1], (j * self.sizeImage[0] + self.dx, i * self.sizeImage[1] + self.dy))
        #self.win.blit(self.images[1], (self.posStart[1] * self.sizeImage[0], self.posStart[0] * self.sizeImage[1]))
        self.win.blit(self.images[0], (self.posEnd[1] * self.sizeImage[0] + self.dx, self.posEnd[0] * self.sizeImage[1] + self.dy))
    
    def DrawPlayers(self):
        self.win.blit(self.images[2],(self.player[0]*self.sizeImage[0] + self.dx, self.player[1]*self.sizeImage[1] + self.dy))
          
    def DrawBot(self):
        for i, j in self.info.items():
            self.win.blit(j[3],(j[0][j[1]][1]*self.sizeImage[0] + self.dx, j[0][j[1]][0]*self.sizeImage[1] + self.dy))
            
    def Dfs(self):
        self.info["dfs"][0].append(tuple(self.posStart))
        depth = [tuple(self.posStart)]
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        visited = set()
        visited.add(tuple(self.posStart))

        while self.info["dfs"][0][-1] != tuple(self.posEnd):
            x, y = self.info["dfs"][0][-1]
            foundMove = False
            random.shuffle(moves)
            random.shuffle(moves)
            for d in moves:
                nx, ny = x + d[0], y + d[1]
                if 0 <= nx < self.sizeMap[0] and 0 <= ny < self.sizeMap[1]:
                    if (nx, ny) not in visited and self.map[nx][ny] != 1:
                        visited.add((nx, ny))
                        self.info["dfs"][0].append((nx, ny))
                        depth.append((nx, ny))
                        foundMove = True
                        break
            
            if not foundMove:
                if depth:
                    depth.pop()
                if depth:
                    self.info["dfs"][0].append(depth[-1])
                else:
                    break
    
    def Bfs(self):
        queue = deque([tuple(self.posStart)])
        visited = set()
        visited.add(tuple(self.posStart))
        parent = {}
        parent[tuple(self.posStart)] = None
        moves = [(0, -1), (-1, 0), (0, 1), (1, 0)]

        while queue:
            x, y = queue.popleft()
            if (x, y) == tuple(self.posEnd):
                break
            random.shuffle(moves)   
            for d in moves:
                nx, ny = x + d[0], y + d[1]
                
                if 0 <= nx < self.sizeMap[0] and 0 <= ny < self.sizeMap[1]:
                    if (nx, ny) not in visited and self.map[nx][ny] != 1:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        parent[(nx, ny)] = (x, y)

        current = tuple(self.posEnd)
        while current:
            self.info["bfs"][0].append(current)
            current = parent[current]
        self.info["bfs"][0].reverse()
    
    def Heuristic(self, current, next):
        pass

    def FindIntersection(self):
        pass

    def Greendy(self):
        pass

    def Ucs(self):
        pass

    def AStart(self):
        pass

    def RenderText(self):
        textRender = self.font.render("Time: " + str(self.time // 60) + "s", True, (0, 0, 0))
        self.win.blit(textRender,(1000, 50))
        for i in range(0, 3):
            textRender = self.font.render(self.text[i], True, (0, 0, 0))
            self.win.blit(textRender,(1000, i*150 + 150))
            if not self.playerFinish and self.text[i] == "Player: ":
                self.win.blit(self.images[i + 2], (1100, i*150 + 145))

            if not self.info["dfs"][2] and self.text[i] == "Dfs: ":
                self.win.blit(self.info["dfs"][3], (1100, i*150 + 145))

            if not self.info["bfs"][2] and self.text[i] == "Bfs: ":
                self.win.blit(self.info["bfs"][3], (1100, i*150 + 145))

    def CheckWinBot(self):
        if self.info["dfs"][1] == len(self.info["dfs"][0]) - 1 and not self.info["dfs"][2]:
            self.text[1] += str(self.finished) + " T: " + str(self.time // 60) + "s"
            self.finished += 1
            self.info["dfs"][2] = True

        if self.info["bfs"][1] == len(self.info["bfs"][0]) - 1 and not self.info["bfs"][2]:
            self.text[2] += str(self.finished) + " T: " + str(self.time // 60) + "s"
            self.finished += 1
            self.info["bfs"][2] = True

    def MovePlayer(self):
        if self.map[self.player[1] + self.vec[1]][self.player[0] + self.vec[0]] == 0 or self.map[self.player[1] + self.vec[1]][self.player[0] + self.vec[0]] == 2:
            self.player[0] += self.vec[0]
            self.player[1] += self.vec[1]
            
        if self.player[0] == self.posEnd[1] and self.player[1] == self.posEnd[0] and not self.playerFinish:
            self.text[0] += str(self.finished) + " T: " + str(self.time // 60) + "s"
            self.finished += 1
            self.playerFinish = True
        
    def MoveBots(self):
        if self.time / 10 > self.info["dfs"][1] and not self.info["dfs"][2]:  
            self.info["dfs"][1] += 1           

        if self.time / 10 > self.info["bfs"][1] and not self.info["bfs"][2]:
            self.info["bfs"][1] += 1

    def CheckEnd(self):
        if self.playerFinish and self.info["dfs"][2] and self.info["bfs"][2]:
            textRender = self.font.render("End Game", True, (0, 0, 0))
            self.win.blit(textRender,(1010, 550))
            pygame.display.update()
            return True
        return False

    def Run(self):
        self.win.fill((255, 255, 255))
        self.DrawMap()
        pygame.display.update()
        pygame.time.delay(3000)
        while self.running:
            self.CheckEnd()
            self.vec[0], self.vec[1] = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
     
                if event.type == pygame.KEYDOWN and not self.playerFinish:
                    if event.key == pygame.K_a:  
                        self.vec[0] = -1
                    elif event.key == pygame.K_d:  
                        self.vec[0] = 1
                    elif event.key == pygame.K_w:  
                        self.vec[1] = -1
                    elif event.key == pygame.K_s: 
                        self.vec[1] = 1

            if (self.CheckEnd()):
                pygame.time.delay(10000)
                self.running = False
            self.win.fill((255, 255, 255))
            self.DrawMap()
            self.DrawBot()
            self.DrawPlayers()
            self.CheckWinBot()
            self.MovePlayer()
            self.MoveBots()
            self.RenderText()
            self.fps.tick(60)
            pygame.display.update()
            self.time += 1

if "__main__" == __name__:
    run = GameAI()
    run.CreateMap()
    run.Dfs()
    run.Bfs()
    run.Run()
