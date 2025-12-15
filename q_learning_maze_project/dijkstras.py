
from pickle import FALSE
from numpy import argmax
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
from old_qlearn_stuff.env import environment, rewards, UP, DOWN, LEFT, RIGHT, FREE,WALL,PACKAGE,DROPOFF
import heapq
from typing import final
# import imageio


class dijkstra_pathfinder():
    def __init__(
            self,
            env:environment,
            ):
        self.env = env
        #eight neighbours
        self.NEIGHBOURS = [(0,1,1),(0,-1,1),(1,0,1),(-1,0,1),
              (1,1,np.sqrt(2)),(-1,-1,np.sqrt(2)),(-1,1,np.sqrt(2)),(1,-1,np.sqrt(2))]
        
    def cost_fn(self,x,y,nx,ny,w):
        return w

    def not_in_bounds(self,x,y):
        if x > (self.env.width -1) or y > (self.env.height -1) or x <0 or y < 0:
            return True
        else:
            return False

    def dijkstra_path(self,start:tuple[int,int],goal:tuple[int,int]):
        start_x, start_y = start
        goal_x, goal_y = goal

        INF = float('inf')
        env = self.env

        dist = [[INF]*env.width for _ in range(env.height)]
        parent = [[None]*env.width for _ in range(env.height)]
        

        pq = [(0,start_x,start_y)]

        while not (len(pq) == 0):
            d, x, y = heapq.heappop(pq)
            if d > dist[y][x]:
                continue 
            if (x, y) == (goal_x, goal_y):
                break

            for (dx, dy , w ) in self.NEIGHBOURS:
                nx,ny = x+dx,y+dy
                if self.not_in_bounds(nx,ny):continue
                if env.grid[nx,ny] == WALL:continue

                step_cost = self.cost_fn(x,y,nx,ny,w)
                nd = d + step_cost
                if nd < dist[ny][nx]:
                    dist[ny][nx] = nd
                    parent[ny][nx] = (x, y)
                    heapq.heappush(pq, (nd, nx, ny))

        return dist,parent

    def reconstruct_path(self,parent,start,goal):
        path = []
        x,y = goal
        while True:
            path.append((x,y))
            if (x,y) == start:
                break
            p = parent[y][x]
            if p is None:
                return []
            x,y =p

        path.reverse()
        return path
    
    def get_next_target(self):
        return None
    

@final
class dijkstra_agent(dijkstra_pathfinder):
    def __init__(self,env:environment):
        super().__init__(env)
        self.num_points = 0
        self.target : tuple[int,int] = (0,0)
        self.pos : tuple[int,int] = (0,0)
        self.is_carrying :bool = False
        self.path = []
        self.colour = 'red'
        self.done = False

    def change_colour_to_blue(self):
        self.colour = 'blue'

    def change_colour_to_red(self):
        self.colour = 'red'
        

    def find_target_and_set_course(self):

        if self.is_carrying:
            self.change_colour_to_blue(self)
            self.target = self.env.drop_off
        else:
            self.target = self.env.package

        dist,parent = self.dijkstra_path(self.pos,self.target)
        self.path = self.reconstruct_path(parent,self.pos,self.target)



    def get_state(self):
        return (self.pos,self.target,self.is_carrying)
    
    def step_along_path(self):
        if len(self.path) != 0:   
            self.pos = self.path[1] #is the next step in the pat
        else:
            print(f"at end of path   target: {self.target}  |   pos: {self.pos}  |  steps along path: {self.steps_along_path}  |  path len: {len(self.path)}")
            self.is_carrying = True












