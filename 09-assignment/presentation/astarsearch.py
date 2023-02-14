# Prioritní prohledávání - priority search
# 
# Jan Kybic, 2016

import heapq
from dfs2 import find_path
from prioritysearch import HeapQItem

def solve(problem,maxdepth=100):
    """ Prohledá stavový prostor z počátečního stavu 'problem' (viz. kozavlkzeli.py) do hloubky nanejvýše 'maxdepth'.
        Vrátí posloupnost stavu (states) vedoucí k řešení nebo 'None'. Stavy musí podporovat metodu '.cost()'
        dodávající odhad ceny k cíli. Používá A* algoritmus, každý krok má jednotkovou cenu. """
    visited={}                     # již navštívené stavy včetně předchůdce
    waiting=[]                     # waiting = vnořená struktura (cena,(stav,předchůdce,úroveň))
    heapq.heappush(waiting,HeapQItem(problem.cost(),(problem,None,0)))   
    numvisited=0
    while len(waiting)>0:
      numvisited+=1
      state,prev,level=heapq.heappop(waiting).get()  # nový stav k uvážení
      if state not in visited:    # je opravdu nový?
        visited[state]=prev       # zapamatujeme si přechůdce 
        if state.final():         # koncový stav?
          print("Navštíveno ",numvisited," stavů.")
          return find_path(state,visited)
        if level<maxdepth:
          for s in state.succ():
            heapq.heappush(waiting,HeapQItem(s.cost()+level,(s,state,level+1)))  
    return None                 # řešení nenalezeno   
      

  
