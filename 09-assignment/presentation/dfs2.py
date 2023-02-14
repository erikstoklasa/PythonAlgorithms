# Prohledávání do hloubky - depth first search
# Nerekurzivní implementace
# Jan Kybic, 2016

import stack

def all_states(problem,maxdepth=10):
  """ Najde všechny možné stavy z počátečního stavu 'problem' do hloubky nanejvýše 'maxdepth'. """
  visited=set()                  # již navštívené stavy
  waiting=stack.Stack()          # waiting = dvojice (stav,úroveň)
  waiting.push((problem,0))
  while not waiting.is_empty():
    state,level=waiting.pop()  # nový stav ke zpracování
    if state not in visited:
      visited|={state}   # označ stav jako navštívený (uzavřený)
      if level<maxdepth:
        for s in state.succ():
          waiting.push((s,level+1))  
  return visited

def print_all_states(problem,maxdepth=10):
  """ Vytiskni všechny stavy z počátečního """
  states=all_states(problem,maxdepth=maxdepth)
  for s in states:
    print(s," -> ",", ".join(map(str,s.succ())))

def solve(problem,maxdepth=10):
    """ Prohledá stavový prostor z počátečního stavu 'problem' (viz. kozavlkzeli.py) do hloubky nanejvýše 'maxdepth'.
        Vrátí posloupnost stavu (states) vedoucí k řešení nebo 'None' """
    visited={}                     # již navštívené stavy včetně předchůdce
    waiting=stack.Stack()          # waiting = trojice (stav, předchůdce,úroveň)
    waiting.push((problem,None,0))   
    numvisited=0
    while not waiting.is_empty():
      numvisited+=1
      state,prev,level=waiting.pop()    # nový stav k uvážení
      if state not in visited:    # je opravdu nový?
        visited[state]=prev       # zapamatujeme si přechůdce 
        if state.final():         # koncový stav?
          print("Navštíveno ",numvisited," stavů.")
          return find_path(state,visited)
        if level<maxdepth:
          for s in state.succ():
            waiting.push((s,state,level+1))  
    return None                 # řešení nenalezeno   
      
def find_path(state,visited):
  """ Vrátí posloupnost stavů od počátečního k cílovému 'state',
      ve mapě 'visited' jsou předchůdci """
  path=[]
  while state is not None:
    path+=[state]         # přidávat dozadu je efektivnější
    state=visited[state]
  return list(reversed(path))  
  
