import random as rand
import time
from collections import deque

def creategraph(length):
    E = {(0,0)}
    que = [(0,0)]
    G = {}
    for x in range(length):
        for y in range(length):
            G[(x,y)] = []
    while len(que) > 0:
        exploring = que[-1]
        explorable = []
        nextnode = (exploring[0]-1, exploring[1])
        if nextnode not in E and nextnode in G:
            explorable.append(nextnode)
        nextnode = (exploring[0]+1, exploring[1])
        if nextnode not in E and nextnode in G:
            explorable.append(nextnode)
        nextnode = (exploring[0], exploring[1]-1)
        if nextnode not in E and nextnode in G:
            explorable.append(nextnode)
        nextnode = (exploring[0], exploring[1]+1)
        if nextnode not in E and nextnode in G:
            explorable.append(nextnode)
        if len(explorable) > 0:
            adding= rand.choice(explorable)
            G[exploring].append(adding)
            G[adding].append(exploring)
            que.append(adding)
            E.add(adding)
        else:
            que.pop()
    return G



def BFS_with_distance(G, s):

    dist = {s:0}
    
    Q = deque([s])

    while len(Q) > 0:
        V = Q.popleft()
        for node in G[V]:
            if node not in dist:
                dist[node] = dist[V] + 1
                Q.append(node)


    return dist

import pygame 
pygame.font.init()
# Define the background colour 
# using RGB color coding. 
background_colour = (255, 255, 255) 
  
# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode((1000, 800)) 
  
# Set the caption of the screen 
pygame.display.set_caption('G') 
alltimes =[]
#time.sleep(10)
for graphs in range(10):
    
    length = 15
    G = creategraph(length)
    dist = BFS_with_distance(G, (0,0))
    furthest = (0, 0)
    for y in range(length):
            if dist[(length-1,y)] > furthest[0]:
                furthest = (dist[(length-1,y)], (length-1,y), (25, 0))
    for x in range(length):
        if dist[(x,length-1)] > furthest[0]:
                furthest = (dist[(x,length-1)], (x, length-1), (0, 25))
    
    
    
      
    # Fill the background colour to the screen 
    screen.fill(background_colour) 
    
    # Update the display using flip 
    pygame.display.flip() 
    
    offset = 50
    scale = 50
    rect = (25,25,length*50,length*50)
    pygame.draw.rect(screen, (0,0,0), rect)
    for loc in G:
        pygame.draw.circle(screen, (255,255,255), (loc[0]*50+50, loc[1]*50+50), 10)
        
        for end in G[loc]:
            pygame.draw.line(screen, (255, 255, 255), 
                             (end[0]*scale+offset, end[1]*scale+offset),
                             (loc[0]*scale+offset, loc[1]*scale+offset), 22)
        pygame.draw.circle(screen, (0,0,255), (loc[0]*50+50, loc[1]*50+50), 5)
    pygame.draw.line(screen, (255, 255, 255), (0, 50), (50, 50), 22)
    pygame.draw.line(screen, (255,255,255), 
                     (furthest[1][0]*scale+offset+furthest[2][0], furthest[1][1]*scale+offset+furthest[2][1]), 
                     (furthest[1][0]*scale+offset, furthest[1][1]*scale+offset), 22)



    running = True
    num =1
    E = [{(0,0)}]
    que = [[(0,0)]]
    locations = [(0,0)]
    
    count = 0
    timeadded = 0
    bouncetime = 0
    while running: 
        pygame.draw.rect(screen, (0,0,0), rect)
        count += 1
        if count % 10 == 0:
            E.append({0,0})
            que.append([(0,0)])
            locations.append([(0,0)])
        for loc in G:
            pygame.draw.circle(screen, (255,255,255), (loc[0]*50+50, loc[1]*50+50), 10)
            for end in G[loc]:
                pygame.draw.line(screen, (255, 255, 255), (end[0]*50+50, end[1]*50+50), (loc[0]*50+50, loc[1]*50+50), 22)
        pygame.draw.line(screen, (255, 255, 255), (0, 50), (50, 50), 22)
        pygame.draw.line(screen, (255,255,255), (furthest[1][0]*scale+offset+furthest[2][0], furthest[1][1]*scale+offset+furthest[2][1]), (furthest[1][0]*scale+offset, furthest[1][1]*scale+offset), 22)

        for i in range(len(que)):
            if len(que[i]) > 0:
                
                exploring = que[i][-1]
        
                pygame.draw.circle(screen, (0,255,0), (exploring[0]*50+50, exploring[1]*50+50), 10)
                pygame.display.update()
                if exploring == furthest[1]:
                    que[i] = []
                    print(f"Person {i} finished at {count} in {count-i*10} steps")
                    continue
                for person in range(len(que)):
                    if exploring == locations[person] and person != i:
                        #print(i, person, exploring)
                        added = False
                        for node in E[person]:
                            if node not in E[i]:
                                E[i].add(node)
                                added = True
                        for node in E[i]:
                            if node not in E[person]:
                                E[person].add(node)
                                added = True
                        if added:
                            pygame.draw.circle(screen, (255,0,0), 
                                               (exploring[0]*50+50, exploring[1]*50+50), 15)
                            time.sleep(0.02)

                explorable = []
                for new in G[exploring]:
                    if new not in E[i]:
                        explorable.append(new)
                if len(explorable) > 0:
                    adding= rand.choice(explorable)
                    que[i].append(adding)
                    E[i].add(adding)
                    locations[i] = adding
                    
                else:
                    que[i].pop()
        time.sleep(0.01)

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
