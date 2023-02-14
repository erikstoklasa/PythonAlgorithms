# Prohledávání do šířky - breadth first search
# Nerekurzivní implementace
# Jan Kybic, 2016

import knuthqueue as queue
from dfs2 import find_path

def all_states(problem,maxdepth=100):
  """ Najde všechny možné stavy z počátečního stavu 'problem' do hloubky nanejvýše 'maxdepth',
      pomocí prohledávání do šířky """
  visited=set()                  # již navštívené stavy
  waiting=queue.Queue()          # waiting = dvojice 
  waiting.enqueue((problem,0))
  while not waiting.is_empty():
    state,level=waiting.dequeue()  # nový stav ke zpracování
    if state not in visited:
      visited|={state}   # označ stav jako navštívený (uzavřený)
      if level<maxdepth:
        for s in state.succ():
          waiting.enqueue((s,level+1))  
  return visited

def print_all_states(problem,maxdepth=100):
  """ Vytiskni všechny stavy z počátečního """
  states=all_states(problem,maxdepth=maxdepth)
  for s in states:
    print(s," -> ",", ".join(map(str,s.succ())))

def solve(problem,maxdepth=100):
    """ Prohledá stavový prostor z počátečního stavu 'problem' (viz. kozavlkzeli.py) do hloubky nanejvýše 'maxdepth'.
        Vrátí posloupnost stavu (states) vedoucí k řešení nebo 'None' """
    visited={}                     # již navštívené stavy včetně předchůdce
    waiting=queue.Queue()          # waiting = dvojice (stav, předchůdce,úroveň)
    waiting.enqueue((problem,None,0))   
    numvisited=0
    while not waiting.is_empty():
      numvisited+=1
      state,prev,level=waiting.dequeue()    # nový stav k uvážení
      # print("state=",str(state)," level=",level)
      if state not in visited:    # je opravdu nový?
        visited[state]=prev       # zapamatujeme si přechůdce 
        if state.final():         # koncový stav?
          print("Navštíveno ",numvisited," stavů.")
          return find_path(state,visited)
        if level<maxdepth:
          for s in state.succ():
            waiting.enqueue((s,state,level+1))  
    return None                 # řešení nenalezeno   
      

  
