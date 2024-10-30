import pygame
import random
import numpy as np
from collections import deque
import math

class GameAI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Game AI")
        self.fps = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.menu = True
        self.createMap = False
        self.isDragging = False
        self.mouseThroughRect = []
        self.rectMenu = [pygame.Rect(500, 100, 200 ,100), pygame.Rect(500, 300, 200 ,100), pygame.Rect(500, 500, 200 ,100)]
        self.textMenu = ["Start", "Create Map", "Exit"]
        self.text = ["Player: ", "Dfs: ", "Bfs: "]
        self.textCreateMap = [ "Press and drag the mouse to", "select the region", 
                            "after selected a region",
                            "Press 1 to set the start position",
                            "Press 2 to set the end position",
                            "Press 3 to create a wall",
                            "Press 4 to delete"
                            ]
        self.sizeMap = [29, 29]
        self.rectMap = []
        self.running = True
        self.time = 0
        self.start = False
        self.end = False
        self.map = np.ones((self.sizeMap[0], self.sizeMap[1]), dtype=int)
        self.sizeImage = [27, 27]
        self.posStart = [5, 5]
        self.posEnd = [26, 19]
        self.movePlayer = 0
        self.player = [5, 5]
        self.vec = [0, 0]
        self.playerFinish = False
        self.finished = 1
        self.info = {
            "dfs": [[], 0, False, pygame.transform.scale(pygame.image.load("images/dfs.png"), (self.sizeImage[0], self.sizeImage[1])), (255, 0, 0), pygame.rect.Rect(870, 1*100 + 150, 20, 20), False],
            "bfs": [[], 0, False,  pygame.transform.scale(pygame.image.load("images/bfs.png"), (self.sizeImage[0], self.sizeImage[1])), (255, 0, 0), pygame.rect.Rect(870, 2*100 + 150, 20, 20), False],
            #"greendy": [[], 0, False,  pygame.transform.scale(pygame.image.load("images/bfs.png"), (self.sizeImage[0], self.sizeImage[1]))],
            }
        self.dx = 65
        self.dy = 10
        self.images = [
            pygame.transform.scale(pygame.image.load("images/finish.png"), (self.sizeImage[0], self.sizeImage[1])),
            pygame.transform.scale(pygame.image.load("images/10.png"), (self.sizeImage[0], self.sizeImage[1])),
            pygame.transform.scale(pygame.image.load("images/player.png"), (self.sizeImage[0], self.sizeImage[1])),
            pygame.transform.scale(pygame.image.load("images/bg.png"), (1190, 800)),
        ]

    # Algorithm
    def Heuristic(self):
        pass

    def FindIntersection(self):
        pass

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
            try:
                current = parent[current]
            except:
                return False
        self.info["bfs"][0].reverse()
        return True

    def Greendy(self):
        pass

    def Hillclimbing(self):
        pass
                
    def AStart(self):
        pass

    ## Stactic Display 
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

    def CheckCreateMap(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.isDragging:
                self.isDragging = True

            elif event.type == pygame.MOUSEBUTTONUP and self.isDragging:
                self.isDragging = False

            elif event.type == pygame.MOUSEMOTION and self.isDragging:
                mousePos = pygame.mouse.get_pos()
                for row in self.rectMap:
                    for rect in row:
                        if rect.collidepoint(mousePos) and rect not in self.mouseThroughRect:
                            self.mouseThroughRect.append(rect)
                
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_s:
                    if self.Bfs():              
                        self.Dfs()
                        self.menu = False
                        self.createMap = False
                    else:
                        font = pygame.font.Font(None, 40)
                        textRender = font.render("No Way", True, (0, 0, 0))
                        self.win.blit(textRender, ((1200 - textRender.get_size()[0]) / 2, 400))
                        pygame.display.update()
                        pygame.time.delay(2000)

                elif event.key == pygame.K_1 and not self.isDragging and len(self.mouseThroughRect) == 1: 
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] == self.mouseThroughRect[0]:                             
                                self.map[self.posStart[0]][self.posStart[1]] = 0
                                self.posStart[0] = i
                                self.posStart[1] = j
                                self.player[0] = j
                                self.player[1] = i
                                self.map[self.posStart[0]][self.posStart[1]] = 0
                                self.start = False
                                self.mouseThroughRect.clear()
                                return
                                
                elif event.key == pygame.K_2 and not self.isDragging and len(self.mouseThroughRect) == 1: 
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] == self.mouseThroughRect[0]:      
                                self.map[self.posEnd[0]][self.posEnd[1]] = 0
                                self.posEnd[0] = i
                                self.posEnd[1] = j
                                self.map[self.posEnd[0]][self.posEnd[1]] = 0
                                self.end = False
                                self.mouseThroughRect.clear()
                                return
                            
                        
                elif event.key == pygame.K_3 and not self.isDragging and len(self.mouseThroughRect) > 0:
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] in self.mouseThroughRect:
                                self.map[i][j] = 1
                    self.mouseThroughRect.clear()            
                elif event.key == pygame.K_4 and not self.isDragging and len(self.mouseThroughRect) > 0: 
                    for i in range(0, len(self.rectMap)):
                        for j in range(0, len(self.rectMap)):
                            if self.rectMap[i][j] in self.mouseThroughRect:
                                self.map[i][j] = 0
                    self.mouseThroughRect.clear()

    def RenderMenu(self):
        self.win.blit(self.images[3], (0, 0))
        for i in range(0, len(self.rectMenu)):
            self.font.bold = False
            textRender = self.font.render(self.textMenu[i] , True, (0, 0, 0))
            size = textRender.get_size()
            self.win.blit(textRender, (400 + (400 - size[0])/2, self.rectMenu[i].centery - textRender.get_size()[1] // 2))
    
    def RenderText(self):
        textRender = self.font.render("Time: " + str(self.time // 60) + "s", True, (0, 0, 0))
        self.win.blit(textRender,(970, 50))
        for i in range(0, 3):
            textRender = self.font.render(self.text[i], True, (0, 0, 0))
            self.win.blit(textRender,(910, i*100 + 150))
            if not self.playerFinish and self.text[i] == "Player: ":
                self.win.blit(self.images[i + 2], (1000, i*100 + 145))

            if not self.info["dfs"][2] and self.text[i] == "Dfs: ":
                pygame.draw.rect(self.win, self.info["dfs"][4], self.info["dfs"][5], 10, 8)
                self.win.blit(self.info["dfs"][3], (1000, i*100 + 145))

            if not self.info["bfs"][2] and self.text[i] == "Bfs: ":
                pygame.draw.rect(self.win, self.info["bfs"][4], self.info["bfs"][5], 10, 8)
                self.win.blit(self.info["bfs"][3], (1000, i*100 + 145))

    def RenderTextCreateMap(self):
        font = pygame.font.Font(None, 28)
        pygame.draw.rect(self.win, (255, 0, 0), pygame.rect.Rect(870, 120, 305, 200), 3)
        for i in range(0, len(self.textCreateMap)):
            textRender = font.render(self.textCreateMap[i], True, (0, 0, 0))
            if i > 1:
                self.win.blit(textRender,(880, i * 20 + 170))
            else:
                self.win.blit(textRender,(880, i*20 + 130))
        
    def CheckButtonMenu(self, mousePos, click):
        cursorHand = False
        for i in range(0, len(self.rectMenu)):
            if self.rectMenu[i].collidepoint(mousePos) and click:
                if i == 0:
                    self.menu = False
                    self.CreateMap()
                    self.Dfs()
                    self.Bfs()
                elif i == 1:
                    self.map = np.zeros((self.sizeMap[0], self.sizeMap[1]), dtype=int)
                    self.createMap = True
                    for i in range(0, self.sizeMap[0]):
                        temp = []
                        for j in range(0, self.sizeMap[1]):
                            temp.append(pygame.Rect(j * self.sizeImage[0] + self.dx, i * self.sizeImage[1] + self.dy, self.sizeImage[1], self.sizeImage[1]))
                        self.rectMap.append(temp)  
                    return
                elif i == 2:
                    self.running = False

            if self.rectMenu[i].collidepoint(mousePos):
                self.font.bold = True
                cursorHand = True
                textRender = self.font.render(self.textMenu[i] , True, (255, 165, 0))
                size = textRender.get_size()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.win.blit(textRender, (400 + (400 - size[0])/2, self.rectMenu[i].centery - textRender.get_size()[1] // 2))

        if not cursorHand:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    ## Logic
    def MovePlayer(self):
        if self.map[self.player[1] + self.vec[1]][self.player[0] + self.vec[0]] == 0 or self.map[self.player[1] + self.vec[1]][self.player[0] + self.vec[0]] == 2:
            if self.vec[0] != 0 or self.vec[1] != 0:
                self.movePlayer += 1

            self.player[0] += self.vec[0]
            self.player[1] += self.vec[1]
            
        if self.player[0] == self.posEnd[1] and self.player[1] == self.posEnd[0] and not self.playerFinish:
            self.text[0] += str(self.finished) + " T: " + str(self.movePlayer + 1)
            self.finished += 1
            self.playerFinish = True

    def CheckWinBot(self):
        if self.info["dfs"][1] == len(self.info["dfs"][0]) - 1 and not self.info["dfs"][2]:
            self.text[1] += str(self.finished) + " T: " + str(len(self.info["dfs"][0]))
            self.finished += 1
            self.info["dfs"][2] = True

        if self.info["bfs"][1] == len(self.info["bfs"][0]) - 1 and not self.info["bfs"][2]:
            self.text[2] += str(self.finished) + " T: " + str(len(self.info["bfs"][0]))
            self.finished += 1
            self.info["bfs"][2] = True
        
    def CheckOnBot(self, mousePos):
        for i, j in self.info.items():
            if self.info[i][5].collidepoint(mousePos) and self.info[i][6]:
                self.info[i][4] = (255, 0, 0)
                self.info[i][6] = False

            elif self.info[i][5].collidepoint(mousePos) and not self.info[i][6]:
                self.info[i][4] = (0, 255, 0)
                self.info[i][6] = True

    def MoveBots(self):
        for i, j in self.info.items():
            if not self.info[i][2] and self.info[i][6] and self.time % 10 == 0:  
                self.info[i][1] += 1           

    def CheckEndGame(self):
        if self.playerFinish:
            for i, j in self.info.items():
                if not self.info[i][2]:
                    return False

            textRender = self.font.render("End Game", True, (0, 0, 0))
            self.win.blit(textRender,(970, 550))
            pygame.display.update()
            return True

        return False

    ## Dynamic Display
    def DrawRectMap(self):
        pygame.draw.rect(self.win, (0, 255, 255), (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 800), 2, 5)
        for i in range(0, len(self.rectMap)):
            for j in range(0, len(self.rectMap)):
                if self.rectMap[i][j] in self.mouseThroughRect:
                    pygame.draw.rect(self.win, (0, 200, 0), self.rectMap[i][j], 16, 5)
                    
                elif not self.start and [i, j] == self.posStart:
                    pygame.draw.rect(self.win, (30, 144, 255), self.rectMap[i][j], 16, 5)
                    
                elif not self.end and [i, j] == self.posEnd:
                    pygame.draw.rect(self.win, (0, 0, 128), self.rectMap[i][j], 16, 5)
                    
                elif self.map[i][j] == 1:
                    pygame.draw.rect(self.win, (220, 20, 60), self.rectMap[i][j], 16, 5)
                    
                pygame.draw.rect(self.win, (0, 0, 0), self.rectMap[i][j], 1, 5)


    def DrawMap(self):
        pygame.draw.rect(self.win, (0, 255, 255), (self.dx - 10, 0, self.sizeMap[0] * self.sizeImage[0] + 20, 800), 2, 5)
        for i in range(0, self.sizeMap[0]):
            for j in range(0, self.sizeMap[1]):
                if self.map[i][j] == 1:
                    self.win.blit(self.images[1], (j * self.sizeImage[0] + self.dx, i * self.sizeImage[1] + self.dy))
                else:
                    pygame.draw.rect(self.win, (0, 0, 0), pygame.rect.Rect(j * self.sizeImage[0] + self.dx, i * self.sizeImage[1] + self.dy, self.sizeImage[0], self.sizeImage[1]), 1, 5)

        self.win.blit(self.images[0], (self.posEnd[1] * self.sizeImage[0] + self.dx, self.posEnd[0] * self.sizeImage[1] + self.dy))
    
    def DrawPlayers(self):
        self.win.blit(self.images[2],(self.player[0]*self.sizeImage[0] + self.dx, self.player[1]*self.sizeImage[1] + self.dy))
          
    def DrawBot(self):
        for i, j in self.info.items():
            self.win.blit(j[3],(j[0][j[1]][1]*self.sizeImage[0] + self.dx, j[0][j[1]][0]*self.sizeImage[1] + self.dy))

    ##      
    def Run(self):
        while self.running:
            if not self.menu:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
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
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousePos = pygame.mouse.get_pos()
                        self.CheckOnBot(mousePos)

                if (self.CheckEndGame()):
                    pygame.time.delay(5000)
                    self.running = False
                    
                self.win.fill((240, 248, 255))
                self.DrawMap()
                self.DrawBot()
                self.CheckWinBot()
                self.MovePlayer()
                self.DrawPlayers()
                self.MoveBots()
                self.RenderText()
                self.fps.tick(60)
                self.time += 1
            else:
                if self.createMap:
                    self.win.fill((240, 248, 255))
                    self.DrawRectMap()
                    self.RenderTextCreateMap()
                    self.CheckCreateMap()
                    pygame.display.update()
                    continue
                    
                self.win.fill((255, 255, 255))
                self.RenderMenu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    mousePos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.CheckButtonMenu(mousePos, True)
                self.CheckButtonMenu(mousePos, False)
            pygame.display.update()

if "__main__" == __name__:
    run = GameAI()
    run.Run()
