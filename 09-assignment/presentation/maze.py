# Stavový prostor pro bludiště
#
# dokáže řešit úlohy vygenerované pomocí, pokud do nich přidáme S,E
# http://www.delorie.com/game-room/mazes/genmaze.cgi

class Maze:
  """ objekt reprezentující bludiště, načteme ho z textového souboru.
      všechny řádky tohoto souboru musí mít stejnou délku. znak 'S' je počáteční pozice,
      znak 'E' je východ, který máme najít. Mezery jsou volné prostory. Všechny ostatní znaky
      znamenají neprostupnou zeď. Řádkový index je 'y', sloupcový 'x'.
   """
  def __init__(self,filename):
    self.m=list(map(lambda x:x.rstrip('\n'), open(filename,'rt').readlines() ))
    self.ny=len(self.m)
    assert(self.ny>0)
    self.nx=len(self.m[0])
    assert(all(map(lambda r: len(r)==self.nx,self.m)))  # všechny řádky stejně dlouhé
    i="".join(self.m).find('S')  
    assert(i>=0)                           # bludiště musí obsahovat 'S"
    self.sy= i // self.nx                  # pozice S
    self.sx= i %  self.nx
    j="".join(self.m).find('E')            
    assert(j>=0)                           # bludiště musí obsahovat 'E"
    self.ey= j // self.nx                  # pozice E
    self.ex= j %  self.nx

    
  def print(self,path=[],visited={}):
    """ vytiskne bludiště včetně řešení, je-li """
    m=list(map(list,self.m)) # převedeme na seznam seznamů
    for v in visited:        # dokresli probraná pole
      if m[v.y][v.x]==' ':
        m[v.y][v.x]='.'
    for s in path:           # dokreslí cestu
      if m[s.y][s.x]==' ':
        m[s.y][s.x]='#'
    for l in m:
      print("".join(l))
    
class MazeState:
  """ objekt reprezentující pozici v bludišti """
  def __init__(self,maze,y=None,x=None): # 'maze' je typu 'Maze'
    self.maze=maze
    self.x=x if x is not None else maze.sx
    self.y=y if y is not None else maze.sy

  actions=((1,0),(0,1),(-1,0),(0,-1))  # down, right, up, left

  def final(self):
    return self.maze.m[self.y][self.x]=='E'

  def succ(self):
    successors=[]   # následníci současného stavu 
    for dy,dx in self.actions: # možné akce
      y=self.y+dy
      x=self.x+dx
      if (x>=0 and x<self.maze.nx and y>=0 and y<self.maze.ny
             and self.maze.m[y][x] in ' SE'):
        successors+=[MazeState(self.maze,y,x)]
    return successors 

  def cost(self):
    """ Evaluate the cost of the current state """
    return abs(self.x-self.maze.ex)+abs(self.y-self.maze.ey)
      
  def __eq__(self,a):
    return self.x==a.x and self.y==a.y and self.maze==a.maze

  def __hash__(self):
    return hash((self.x,self.y,self.maze))
     
  def __str__(self):
    """ vrátí reprezentaci stavu jako řetězec """
    return "("+str(self.y)+","+str(self.x)+")"

  
##################################################################

import bfs
import dfs
import dfs2
import prioritysearch
import astarsearch

def solve_maze_bfs(filename='maze.txt',maxdepth=500):
  m=Maze(filename)
  sol=bfs.solve(MazeState(m),maxdepth=maxdepth)
  if sol:
    print("Délka cesty=",len(sol))
    m.print(path=sol)
  else:
    print("Řešení nenalezeno.")

def solve_maze_dfs(filename='maze.txt',maxdepth=500):
  m=Maze(filename)
  sol=dfs.solve(MazeState(m),maxdepth=maxdepth)
  if sol:
    print("Délka cesty=",len(sol))
    m.print(path=sol)
  else:
    print("Řešení nenalezeno.")
    
def solve_maze_dfs2(filename='maze.txt',maxdepth=500):
  m=Maze(filename)
  sol=dfs2.solve(MazeState(m),maxdepth=maxdepth)
  if sol:
    print("Délka cesty=",len(sol))
    m.print(path=sol)
  else:
    print("Řešení nenalezeno.")
    
def solve_maze_priority(filename='maze.txt',maxdepth=500):
  m=Maze(filename)
  sol=prioritysearch.solve(MazeState(m),maxdepth=maxdepth)
  if sol:
    print("Délka cesty=",len(sol))
    m.print(path=sol)
  else:
    print("Řešení nenalezeno.")

def solve_maze_astar(filename='maze.txt',maxdepth=500):
  m=Maze(filename)
  sol=astarsearch.solve(MazeState(m),maxdepth=maxdepth)
  if sol:
    print("Délka cesty=",len(sol))
    m.print(path=sol)
  else:
    print("Řešení nenalezeno.")
        

    
    
